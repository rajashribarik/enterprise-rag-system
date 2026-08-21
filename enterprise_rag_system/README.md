# Enterprise RAG System

Production-oriented document question-answering platform built with FastAPI, LangChain, FAISS, Hugging Face embeddings, PostgreSQL-ready metadata, hybrid retrieval hooks, reranking, citations, conversation memory, evaluation utilities, and a Streamlit UI.

## Architecture

Upload documents -> parse/chunk -> embed -> FAISS index -> retrieve -> rerank -> grounded LLM answer -> citations.

## Supported documents

PDF, DOCX, TXT, MD.

## Quick start

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app/streamlit_app.py
```

For the API:

```bash
uvicorn app.api:app --reload
```

Set `HF_TOKEN` if your selected Hugging Face model requires authentication.

## Project structure

- `app/` API and Streamlit application
- `src/` ingestion, retrieval, generation, evaluation and configuration
- `tests/` unit tests
- `data/` local document/index storage
- `scripts/` indexing and evaluation helpers

## Industry-oriented features

- Modular ingestion pipeline
- Persistent FAISS indexes
- Metadata-aware retrieval
- Cross-encoder reranking
- Source citations
- Prompt-injection-aware context handling
- Configurable LLM provider
- FastAPI service layer
- Streamlit client
- Evaluation dataset format
- Docker deployment
- Logging and health endpoint

This repository is designed as a strong portfolio implementation. Before production deployment, add authentication/authorization, secrets management, encrypted storage, observability, rate limiting, malware scanning for uploads, and a managed vector database if required by scale.
