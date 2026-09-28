from pathlib import Path
from functools import lru_cache

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from src.config import settings


@lru_cache(maxsize=1)
def embeddings():
    """Load the embedding model once and reuse it."""
    return HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        encode_kwargs={"normalize_embeddings": True},
    )


def build_index(documents):
    """Build and save a FAISS index."""
    if not documents:
        raise ValueError("No documents were provided for indexing.")

    db = FAISS.from_documents(
        documents,
        embeddings(),
    )

    db.save_local(str(settings.index_dir))

    return db


def load_index():
    """Load the existing FAISS index."""
    index_path = Path(settings.index_dir)

    if not (index_path / "index.faiss").exists():
        raise FileNotFoundError(
            "No index found. Upload and index a document first."
        )

    return FAISS.load_local(
        str(index_path),
        embeddings(),
        allow_dangerous_deserialization=True,
    )
