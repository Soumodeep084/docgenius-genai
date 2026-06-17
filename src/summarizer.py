import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import PromptTemplate

class Summarizer:
    def __init__(self):
        """
        Initialize the Summarizer with necessary components.
        This includes setting up the Hugging Face Inference Client and defining the text splitter.
        """
        # Initialize the Hugging Face Inference Client
        load_dotenv()
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable is not set.")
        
        # Initialize the LLM Model
        self.llm = GoogleGenerativeAI(model="gemini-2.0-flash" , temperature=0.1, api_key=GOOGLE_API_KEY)
        
        # Initialize the text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=4000, 
            chunk_overlap=300
        )
        
        
        # Define the prompt template for question generation
        self.prompt_template = """
            You are an expert summarizer.

           Provide a {summary_length} professional executive summary of the following content. Focus on key points, outcomes, and insights.

            - Avoid unnecessary repetition or filler.
            - Write in **natural, professional English**.
            - Use **complete sentences**, not fragments.

            --- Text to Summarize ---
            {text}

            """
        
        
    def text_extraction_pdf(self, file_path: str) -> list[str]:
        """
        Load a PDF file and extract its text content and return the chunks.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError("PDF file not found.")
        
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        text = "\n".join(doc.page_content for doc in documents)
        
        # Split the text into chunks
        chunks = self.text_splitter.split_text(text)
        
        return chunks
    
    
    def summarize_text(self , text: str, summary_length: str) -> str:
        """
        Define and return a summarization generation chain.
        """
        prompt = PromptTemplate(
            input_variables=["text" , "summary_length"],
            template=self.prompt_template
        )
        chain = prompt | self.llm
        
        try:
            result = chain.invoke({"text": text, "summary_length": summary_length})
            return result
        except Exception as e:
            return "⚠️ AI service is currently unavailable. Please try again later."

    
    def run_pipeline(self, text_type: str, input_data: str, summary_length: str) -> str:
        """
        Run the entire pipeline: extract or process text, generate questions and answers.
        :param text_type: 'pdf' for file path, 'text' for direct string input
        :param input_data: PDF path if text_type is 'pdf', else raw string if 'text'
        :return: Summary
        """
        
        if text_type not in ["pdf", "text"]:
            raise ValueError("Unsupported input type. Use 'pdf' for file path or 'text' for raw input.")

        # Step 1: Get the chunks
        if text_type == "pdf":
            docs = self.text_extraction_pdf(input_data)
        else:
            # If the input is a string, split it into chunks
            docs = self.text_splitter.split_text(input_data)

        # Step 2: Check Chunks and Get the Summaries
        if not docs:
            raise ValueError("No content found in the input data.")
        
        final_summary = ""
        
        if len(docs) > 1:
            # If there are multiple chunks, summarize each chunk
            summaries = [self.summarize_text(doc , summary_length) for doc in docs]
            total_summaries = "\n".join(summaries)
            
            # Summarize the combined summaries
            final_summary = self.summarize_text(total_summaries , summary_length)
        else:
            # If there's only one chunk, summarize it directly
            final_summary = self.summarize_text(docs[0] , summary_length)
            
        return final_summary


