import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class QAGenerator:
    def __init__(self):
        """
        Initialize the QAGenerator with necessary components.
        This includes loading environment variables, initializing the LLM model,
        setting up the text splitter, and defining the prompt template for question generation.
        """
        
    
        # Load environment variables
        load_dotenv()
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable is not set.")
        
        # Initialize the LLM Model
        self.llm = GoogleGenerativeAI(model="gemini-2.0-flash" , temperature=0.1, api_key=GOOGLE_API_KEY)
        
        # Initialize the text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000, 
            chunk_overlap=200
        )
        
        # Define the prompt template for question generation
        self.prompt_template: str = """
            You are an expert at generating questions and answers from any educational or informative content.
            Your goal is to help learners understand and prepare for exams or interviews by generating high-quality questions and accurate answers from the provided content.

            ------------
            {text}
            ------------

            Based on the above text, generate EXACTLY {n} question-answer pairs that help the user prepare.
            Make sure the questions cover key points and do not leave out important information.

            Return ONLY the following format.

            Q1:
            A1:

            Q2:
            A2:
            ... and so on up to {n} pairs.
            
            Do not include introductions.
            Do not include markdown.
            Do not include bullet points.
            Do not include explanations.
            """
        
    def prepare_text_documents(self , text: str) -> list[Document]:
        """
        Process a text and split it into chunks.
        """
        
        if not text.strip():
            raise ValueError("Input text cannot be empty.")
        
        # Split the text into chunks
        chunks = self.text_splitter.split_text(text)
        
        # Create Document objects for each chunk
        docs = [Document(page_content=chunk) for chunk in chunks]
        return docs
    
        
    def text_extraction_pdf(self, file_path: str) -> list[Document]:
        """
        Extract text from a PDF file and Modify it.
        """
        
        # Load the PDF file
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        
        loader = PyPDFLoader(file_path)
        data = loader.load()
        
        # Extract text from the loaded data
        if not data:
            raise ValueError("No content found in the PDF file.")
        
        # Combine all page contents into a single string
        text_data = "\n".join(page.page_content for page in data) 
            
        # Split the text into chunks
        if not text_data.strip():
            raise ValueError("No text data extracted from the PDF file.")
        
        chunks = self.text_splitter.split_text(text_data)
        
        
        # Create Document objects for each chunk
        docs = [Document(page_content=chunk) for chunk in chunks]
        return docs
    
    def define_chain(self):
        """
        Define and return a question-answer generation chain.
        """
        prompt = PromptTemplate(
            input_variables=["text", "n"],
            template=self.prompt_template
        )
        chain = prompt | self.llm
        return chain
    
    def _get_qa_distribution(self, n: int, chunks: int) -> list[int]:
        base = n // chunks
        remainder = n % chunks
        return [base + (1 if i < remainder else 0) for i in range(chunks)]

    def run_pipeline(self, text_type: str, input_data: str, n: int) -> list[dict]:
        """
        Run the entire pipeline: extract or process text, generate questions and answers.
        :param text_type: 'pdf' for file path, 'text' for direct string input
        :param input_data: PDF path if text_type is 'pdf', raw string if 'text'
        :param n: Total number of Q&A pairs desired
        :return: List of Q&A pairs as dicts: [{"key": question, "value": answer}, ...]
        """

        if text_type not in ["pdf", "text"]:
            raise ValueError("Unsupported input type. Use 'pdf' for file path or 'text' for raw input.")

        if n <= 0:
            raise ValueError("Number of questions must be greater than zero.")
        
        # Step 1: Get the Document chunks
        if text_type == "pdf":
            docs = self.text_extraction_pdf(input_data)
        else:
            docs = self.prepare_text_documents(input_data)

        chunk_len = len(docs)
        if chunk_len == 0:
            return []

        # Step 2: Define the chain
        chain = self.define_chain()
        
        # Step 3: Distribute n QA pairs across chunks
        qa_distribution = self._get_qa_distribution(n, chunk_len)

        # Step 4: Generate QA pairs
        qa_pairs = []

        for doc, n_per_chunk in zip(docs, qa_distribution):
            if n_per_chunk == 0:
                continue

            try:
                result = chain.invoke(
                    {
                        "text": doc.page_content,
                        "n": n_per_chunk
                    }
                )
            except Exception as e:
                raise RuntimeError(f"Failed to generate Q&A pairs: {str(e)}")
            
            # Split result into Q&A pairs
            raw_pairs = result.strip().split("\n\n")

            count = 0
            for pair in raw_pairs:
                if count >= n_per_chunk:
                    break

                lines = pair.strip().split("\n")
                question_line = next(
                    (line for line in lines
                    if line.lower().startswith(("q", "question"))),
                    None
                )

                answer_line = next(
                    (line for line in lines
                    if line.lower().startswith(("a", "answer"))),
                    None
                )

                if question_line and answer_line:
                    question = question_line.split(":", 1)[-1].strip()
                    answer = answer_line.split(":", 1)[-1].strip()
                    qa_pairs.append({"key": question, "value": answer})
                    count += 1

        # Ensure only `n` total QAs are returned
        return qa_pairs[:n]
