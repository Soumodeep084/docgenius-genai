# DocGenius – AI-Powered Document Assistant

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green?logo=fastapi)
![LangChain](https://img.shields.io/badge/LangChain-LLM-orange)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-AI-purple?logo=google)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.7-blueviolet?logo=bootstrap)


**DocGenius** is a Generative AI web application that intelligently summarizes documents and generates Q&A pairs from PDF or raw text input using powerful language models via [LangChain](https://www.langchain.com/). Designed for simplicity and speed, it combines FastAPI on the backend with a responsive frontend built using Jinja2, Bootstrap, and vanilla JavaScript.

---

## 🚀 Features

- 📄 Upload PDF or paste raw text
- ✨ AI-powered document summarization
- ❓ Automatic Q&A pair generation
- ⚡ FastAPI backend (lightweight & fast)
- 🎨 Simple responsive UI (Bootstrap 5)
- 🧠 LangChain-based LLM integration

---

## 🧰 Tech Stack

- **Backend:** FastAPI, Python
- **AI Framework:** LangChain, Google Gemini API
- **Frontend:** HTML, CSS, JavaScript, Bootstrap 5
- **LLM:** Gemini (via langchain-google-genai)
- **File Handling:** PyPDFLoader

---

## 📁 Project Structure

```
backend/
├── Data/                           # Just an Example Pdf
├── Experiment/                     # Performed First The Operations to check
│   ├── qa_generator.ipynb
│   └── Summarizer.ipynb
├── docgenius/                      # Virtual Env File
├── src/
│   ├── __init__.py
│   ├── qa_generator.py
│   └── summarizer.py
├── static/                         # Static Js Files
│   ├── images/
│   └── js/
│       ├── qaGen.js
│       └── summarizer.js
├── templates/                      # Templates for Frontent
│   ├── components/
│   │   ├── qagen.html
│   │   └── summarizer.html
│   └── index.html
├── .env
├── .gitignore
├── app.py
├── installed_packages.txt
├── README.md
└── requirements.txt
```

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Soumodeep084/docgenius-genai.git
cd docgenius-genai/
```

### 2. Create and Activate Virtual Environment

```bash
# Create virtual environment
python -m venv docgenius

# Activate it
# On Windows:
.\docgenius\Scripts\activate

# On macOS/Linux:
source docgenius/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup environment variables

Create a .env file:

```bash
GOOGLE_API_KEY=your_api_key_here
```

---

### 5. Run the application

```bash
uvicorn app:app --reload --port 8080
```

Navigate to: [http://localhost:8080](http://localhost:8080)

---

## 🧠 How It Works

- PDF/Text is split into chunks
- Each chunk is sent to LLM via LangChain
- LLM generates:
  - Summary OR
  - Question-Answer pairs
- Results are displayed in UI dynamically

---

## 📌 Use Cases

- 📚 Students for exam preparation
- 🧾 Quick document understanding
- 🧑‍🏫 Teachers creating Q&A sets
- 💼 Professionals summarizing reports

---

## ⚠️ Notes

- Requires active Gemini API key
- Free-tier API has strict rate limits
- Large documents may take time to process

---

## 🙌 Acknowledgements

- [LangChain](https://www.langchain.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Bootstrap 5](https://getbootstrap.com/)
- [Google Gemini](https://ai.google.dev/gemini-api)
- [Marked.js](https://marked.js.org/) – for markdown-to-HTML rendering
