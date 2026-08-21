# Architecture

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
              +-------------+-------------+
              |                           |
              v                           v
      +---------------+          +----------------+
      | Ingestion     |          | RAG Pipeline   |
      | PDF/DOCX/TXT  |          | Retrieve       |
      +-------+-------+          | Rerank         |
              |                  | Generate       |
              v                  +-------+--------+
      +---------------+                  |
      | Chunk + Embed |                  v
      +-------+-------+           +-------------+
              |                   | Citations   |
              v                   +-------------+
      +---------------+
      | FAISS Index   |
      +---------------+
```

The design intentionally separates ingestion, vector retrieval, reranking, generation and serving so each layer can later be replaced independently.
