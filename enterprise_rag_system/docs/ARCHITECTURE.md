# Architecture

The Enterprise RAG System follows a modular pipeline that separates document ingestion, indexing, retrieval, reranking, generation, and application serving.

## System Architecture

```text
                    +----------------------+
                    | Streamlit Web Client |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |      FastAPI API     |
                    +----------+-----------+
                               |
                +--------------+--------------+
                |                             |
                v                             v
       +----------------+             +----------------+
       | Document       |             | Question       |
       | Upload         |             | /ask           |
       +-------+--------+             +--------+-------+
               |                               |
               v                               v
       +----------------+             +----------------+
       | Background     |             | RAG Pipeline   |
       | Indexing Job   |             |                |
       +-------+--------+             +--------+-------+
               |                               |
               v                               v
       +----------------+             +----------------+
       | Parse + Clean  |             | FAISS Search   |
       | + Chunk        |             +--------+-------+
       +-------+--------+                      |
               |                               v
               v                      +----------------+
       +----------------+              | Cross-Encoder |
       | Hugging Face   |              | Reranking     |
       | Embeddings     |              +--------+-------+
       +-------+--------+                       |
               |                                v
               v                       +----------------+
       +----------------+               | Context       |
       | FAISS Index    |               | Construction   |
       +----------------+               +--------+-------+
                                                |
                                                v
                                       +----------------+
                                       | Groq LLM       |
                                       | Generation     |
                                       +--------+-------+
                                                |
                                                v
                                       +----------------+
                                       | Answer +       |
                                       | Sources        |
                                       +----------------+
```

## Document Indexing Flow

Documents are uploaded through the Streamlit interface and sent to the FastAPI backend.

The API creates a background indexing job and immediately returns a job ID. The Streamlit client polls the job status while the document is processed.

```text
Upload
  ↓
Job Created
  ↓
Document Parsing
  ↓
Text Cleaning
  ↓
Chunking
  ↓
Embedding Generation
  ↓
FAISS Index Creation
  ↓
Indexing Completed
```

This approach prevents large document processing from blocking the upload request.

## Question Answering Flow

Once a document has been indexed, users can submit questions through the Streamlit interface.

```text
User Question
      ↓
FastAPI /ask
      ↓
FAISS Similarity Search
      ↓
Top-K Retrieved Chunks
      ↓
Cross-Encoder Reranking
      ↓
Relevant Context
      ↓
Groq LLM
      ↓
Grounded Answer
      ↓
Retrieved Sources
```

## Modular Design

The project intentionally separates major components so that individual technologies can be replaced independently.

* **FastAPI** — API and service layer
* **Streamlit** — user interface
* **Ingestion** — document loading, cleaning, and chunking
* **Hugging Face** — embedding generation
* **FAISS** — vector similarity search
* **Reranking** — relevance refinement
* **Groq** — LLM response generation
* **Configuration** — environment-based application settings

This modular architecture allows components such as the vector database, embedding model, reranker, LLM provider, or job-processing infrastructure to be replaced as the system scales.

## Production Scaling Considerations

The current implementation uses an in-process background worker for document indexing.

For a production deployment, this component could be replaced with a distributed job-processing system such as a message queue and dedicated worker processes.

Other production considerations include:

* Authentication and authorization
* Persistent job queues
* Document-level access control
* Secure secret management
* Upload validation and malware scanning
* Observability and structured logging
* Rate limiting
* Managed vector storage
* Monitoring and alerting

