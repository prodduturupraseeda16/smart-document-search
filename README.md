# Smart Document Search System 📄🤖

An interactive, AI-powered Retrieval-Augmented Generation (RAG) platform that lets you upload multiple PDF documents and perform semantic search, multi-turn QA chat, and automatic summarization. Powered by Streamlit, LangChain, FAISS, and Groq's high-speed Llama-3 API.

---
## 🚀 Live Demo

Try the working application here:

[Smart Document Search System - Live Demo](https://prodduturupraseeda16-smart-document-search-app-exm0ap.streamlit.app/)

## 📂 Project Architecture & Data Flow

Below is the conceptual architecture of the semantic indexing and conversational retrieval loop:

```text
[PDF Upload] ──> [PyPDFLoader] ──> [Text Splitting] ──> [HuggingFace Embeddings]
                                                                │
                                                                ▼
[Groq LLM Synthesis] <── [FAISS Similarity Search] <── [FAISS Vector Store]
```

1. **Ingestion**: Uploaded PDFs are parsed dynamically and written to temporary paths, parsed into text chunks using standard character delimiters, and vectorized locally.
2. **Indexing**: Clean text vector dimensions (384-dims) are stored inside a session-bound local memory FAISS database.
3. **Retrieval**: User prompts trigger semantic searches over FAISS indices returning top-ranked content chunks coupled with page metadata.
4. **Synthesis**: Relevant context prompts are sent over safe HTTPS channels to the Groq API (Llama-3-70B model) to deliver contextually grounded summaries or answers.

---

## ✨ Features

- **Multi-Document Ingestion**: Upload multiple PDF documents simultaneously.
- **ChatGPT-Style Interface**: Conversational messaging loop using Streamlit's native `chat_input` and `chat_message` layout.
- **Smart Summarization**: Automatic generation of key bullet points highlighting documents.
- **Precision Page Citations**: Displays exact page numbers above referenced snippets, separating distinct sources with visual indicator lines.
- **Resource Caching**: Embedding transformer weights are cached globally across reruns (`@st.cache_resource`) to guarantee optimal system performance.
- **Security & Stability Defenses**: Clean exception containment showing friendly user error notifications while capturing detailed diagnostics trace logs internally.

---

## 🛠️ Tech Stack

- **User Interface**: [Streamlit](https://streamlit.io/)
- **Orchestration Framework**: [LangChain](https://www.langchain.com/)
- **Vector Storage**: [FAISS (Facebook AI Similarity Search)](https://github.com/facebookresearch/faiss)
- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2` (Local execution)
- **Large Language Model API**: [Groq Cloud](https://groq.com/) (`llama-3.3-70b-versatile`)
- **Environment Management**: Python Dotenv

---

## 🚀 Installation & Local Setup

### Prerequisites
- Python 3.9 or higher
- A Groq Cloud API Account (Get your API key [here](https://console.groq.com/))

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/Smart-Document-Search.git
cd Smart-Document-Search
```

### 2. Set Up Virtual Environment
Create and activate a Python virtual environment to manage dependencies:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
Install packages listed inside the `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
Create a file named `.env` in the root directory of the project and populate it with your Groq API credentials:
```env
GROQ_API_KEY=your_groq_api_key_here
```
> ⚠️ **Warning**: Never commit your `.env` file to version control. The `.gitignore` file is configured to exclude `.env` by default.

---

## 💻 How to Run Locally

Launch the Streamlit web dashboard:
```bash
streamlit run app.py
```
After the server initializes, your default web browser will automatically open:
`http://localhost:8501`

1. **Ingest Documents**: Drag-and-drop or upload PDF files in the sidebar and click **Process Documents**.
2. **Summarize**: Click the **Generate Summary** button to see bullet points of the first few sections.
3. **Chat**: Ask questions in the main screen's chat box and review the retrieved page references.

---

## 📸 Screenshots

*(Placeholders for UI demonstration)*

| Side Panel Ingestion Dashboard | Chat Conversational Screen |
| :---: | :---: |
| ![Sidebar UI Placeholder](https://placehold.co/400x300?text=Sidebar+PDF+Uploader) | ![Chat Interface Placeholder](https://placehold.co/400x300?text=ChatGPT-style+Chat+Bubble+View) |

---

## 🔮 Future Enhancements

- **Persistent Vector Indexes**: Support saving FAISS indices to local disk or cloud repositories (e.g., Pinecone or ChromaDB) to preserve user databases across restarts.
- **Scanned Document OCR**: Use OCR frameworks (like Tesseract or EasyOCR) to support reading non-selectable, image-based text files.
- **Hierarchical Summarization**: Upgrade the summary builder using Map-Reduce chains to summarize massive multi-hundred-page files.
- **Hybrid Search**: Combine semantic FAISS vector queries with exact keyword search models (BM25) for more accurate technical terminology retrieval.

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for more details.
