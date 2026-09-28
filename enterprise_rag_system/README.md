# Enterprise RAG System

Production-oriented Retrieval-Augmented Generation (RAG) platform for document ingestion, semantic retrieval, reranking, and grounded question answering.

Built with **FastAPI, Streamlit, LangChain, FAISS, Hugging Face embeddings, and Groq LLMs**.

## Architecture

```text
Document Upload
      ↓
Document Parsing
      ↓
Text Cleaning & Chunking
      ↓
Hugging Face Embeddings
      ↓
FAISS Vector Index
      ↓
Similarity Retrieval
      ↓
Cross-Encoder Reranking
      ↓
Context-Aware Prompt
      ↓
Groq LLM
      ↓
Grounded Answer + Sources
```

## Key Features

* PDF, DOCX, TXT, and Markdown document support
* Background document indexing for large files
* Configurable chunking and retrieval parameters
* Hugging Face sentence-transformer embeddings
* FAISS vector similarity search
* Cross-encoder reranking
* Groq-powered response generation
* Source-aware answers with retrieved document context
* FastAPI REST API
* Streamlit web interface
* Document indexing job status tracking
* Health-check endpoint
* Environment-based configuration
* Modular project architecture
* Docker-ready deployment structure

## Supported Documents

* PDF
* DOCX
* TXT
* Markdown

## Quick Start

### 1. Create a virtual environment

```bash
python -m venv .venv
```

### 2. Activate the environment

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file from `.env.example` and configure your LLM provider and API credentials.

Example:

```env
LLM_PROVIDER=groq
GROQ_API_KEY=your_api_key_here
```

**Never commit `.env` or API keys to GitHub.**

### 5. Start the FastAPI backend

```bash
python -m uvicorn app.api:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

### 6. Start the Streamlit application

Open another terminal:

```bash
streamlit run app/streamlit_app.py
```

The application will be available at:

```text
http://localhost:8501
```

## API Endpoints

| Method | Endpoint                     | Description                                       |
| ------ | ---------------------------- | ------------------------------------------------- |
| GET    | `/health`                    | API health check                                  |
| POST   | `/documents`                 | Upload and start document indexing                |
| GET    | `/documents/status/{job_id}` | Check indexing job status                         |
| POST   | `/ask`                       | Ask a question against the indexed knowledge base |

## Project Structure

```text
enterprise_rag_system/
│
├── app/
│   ├── api.py
│   ├── streamlit_app.py
│   └── __init__.py
│
├── src/
│   ├── config.py
│   ├── ingestion.py
│   ├── vectorstore.py
│   ├── rag.py
│   ├── reranker.py
│   ├── generator.py
│   ├── evaluation.py
│   └── __init__.py
│
├── data/
│   └── evaluation.json
│
├── docs/
├── scripts/
├── tests/
│
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## RAG Pipeline

The system processes documents through the following workflow:

1. Upload a supported document.
2. Extract and clean document text.
3. Split the text into overlapping chunks.
4. Generate vector embeddings.
5. Build and persist a FAISS index.
6. Retrieve relevant chunks for a user query.
7. Rerank retrieved context.
8. Send relevant context to the LLM.
9. Generate a grounded response.
10. Return the answer together with retrieved source information.

## Large Document Processing

Document indexing runs as a background job through the FastAPI service.

Instead of keeping the upload request blocked while a large document is embedded, the API returns a `job_id`. The client can then monitor the indexing status until processing is completed.

Example workflow:

```text
Upload Document
      ↓
Receive Job ID
      ↓
Background Processing
      ↓
Extract & Chunk
      ↓
Build FAISS Index
      ↓
Completed
      ↓
Ask Questions
```

## Configuration

Important settings can be configured through `.env`:

```env
APP_NAME=Enterprise RAG System
LLM_PROVIDER=groq

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
RERANKER_MODEL=cross-encoder/ms-marco-MiniLM-L-6-v2

TOP_K=8
RERANK_TOP_K=4

CHUNK_SIZE=900
CHUNK_OVERLAP=120

INDEX_DIR=data/index
UPLOAD_DIR=data/uploads
```

Do not commit secrets such as:

```text
.env
GROQ_API_KEY
HF_TOKEN
```

## Testing

The project includes a test structure for validating application components and RAG functionality.

For a local test run:

```bash
pytest
```

## Docker

The repository includes Docker configuration for containerized deployment.

```bash
docker compose up --build
```

Docker deployment should be configured with appropriate environment variables and persistent storage for the target environment.

## Production Considerations

This project is designed as a production-oriented portfolio implementation and local demonstration.

For a production deployment, additional infrastructure and security controls should be considered, including:

* Authentication and authorization
* Secret management
* Persistent job queues
* Distributed background workers
* Rate limiting
* Structured logging and observability
* Upload size and resource limits
* Malware and file-content scanning
* Encrypted storage
* Access-controlled document storage
* Managed vector database for larger workloads
* Monitoring and alerting
* Evaluation and RAG quality monitoring

## License

This project is intended for educational, portfolio, and demonstration purposes.
