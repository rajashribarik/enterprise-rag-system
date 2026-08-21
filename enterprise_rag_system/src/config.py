from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Enterprise RAG System"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    reranker_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    llm_provider: str = "mock"
    groq_api_key: str | None = None
    hf_token: str | None = None
    top_k: int = 8
    rerank_top_k: int = 4
    chunk_size: int = 900
    chunk_overlap: int = 120
    index_dir: Path = Path("data/index")
    upload_dir: Path = Path("data/uploads")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
settings.index_dir.mkdir(parents=True, exist_ok=True)
settings.upload_dir.mkdir(parents=True, exist_ok=True)
