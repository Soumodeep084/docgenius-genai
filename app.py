from fastapi import FastAPI, Request, UploadFile, File , Form
from fastapi.responses import HTMLResponse, PlainTextResponse , JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import uvicorn

import tempfile
import shutil

from src.summarizer import Summarizer
from src.qa_generator import QAGenerator

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/component/{name}", response_class=HTMLResponse)
async def get_component(name: str):
    path = f"templates/components/{name}.html"
    if not os.path.exists(path):
        return PlainTextResponse("Component not found", status_code=404)
    with open(path, "r") as file:
        return HTMLResponse(content=file.read())


@app.post("/summarize/pdf")
async def summarize_pdf(file: UploadFile = File(...) , summary_length: str = Form(...)):
    # Step 1: Save the uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        temp_file_path = tmp.name  # Get the temp file path
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    # Step 2: Initialize your Summarizer and run the pipeline
    summarizer = Summarizer()
    summary = summarizer.run_pipeline(text_type="pdf", input_data=temp_file_path, summary_length=summary_length)

    # Optional: Clean up the temp file 
    os.remove(temp_file_path)

    # Step 3: Return the result
    return PlainTextResponse(summary)


@app.post("/summarize/text")
async def summarize_text(text: str = Form(...), summaryLength: str = Form(...)):
    # Step 2: Initialize your Summarizer and run the pipeline
    summarizer = Summarizer()
    summary = summarizer.run_pipeline(text_type="text", input_data=text, summary_length=summaryLength)
    
    return PlainTextResponse(summary)


@app.post("/qa_gen/pdf")
async def qa_pdf(file: UploadFile = File(...) , n: int = Form(...)):
    # Step 1: Save the uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        temp_file_path = tmp.name  # Get the temp file path
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    # Step 2: Initialize your QAGenerator and run the pipeline
    qa_generator = QAGenerator()
    qa_pairs = qa_generator.run_pipeline(text_type="pdf", input_data=temp_file_path, n=n)
    
    # Step 3: Optional cleanup of the temp file
    os.remove(temp_file_path)
    
    # Step 4: Return the result
    if not qa_pairs:
        return PlainTextResponse("No Q&A pairs generated from the PDF.", status_code=404)
    
    # Step 5: Return the QA Pair List
    return JSONResponse(content = qa_pairs)


@app.post("/qa_gen/text")
async def qa_text(text: str = Form(...) , n: int = Form(...)):
    
    # Step 1: Validate input data
    if not text.strip():
        return PlainTextResponse(
            "No text provided for Q&A generation.",
            status_code=400
        )
    
    # Step 2: Initialize your QAGenerator and run the pipeline
    qa_generator = QAGenerator()
    qa_pairs = qa_generator.run_pipeline(text_type="text", input_data=text, n=n)
    
    # Step 3: Return the result
    if not qa_pairs:
        return PlainTextResponse("No Q&A pairs generated from the text.", status_code=404)
    
    # Step 4: Return the QA Pair List as a string

    return JSONResponse(content = qa_pairs)


if __name__ == "__main__":
    uvicorn.run("app:app", host='0.0.0.0', port=8080, reload=True)