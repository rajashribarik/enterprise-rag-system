from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import settings


def clean_text(text: str) -> str:
    """Clean common PDF text extraction artifacts."""

    replacements = {
        "\u00e2\u00af": " ",
        "\u00e2\u20ac\u2122": "'",
        "\u00e2\u20ac\u0153": '"',
        "\u00e2\u20ac\u009d": '"',
        "\u00e2\u20ac\u201c": "-",
        "\u00e2\u20ac\u201d": "-",
        "\u00e2\u20ac\u00a6": "...",
        "\u00c2": "",
        "\u00c3\u00a9": "e",
        "\u00c3\u00a8": "e",
        "\u00c3\u00a1": "a",
        "\u00c3\u00b3": "o",
        "\u00c3\u00b1": "n",
        "\u00c3\u00bc": "u",
        "\u00c3\u00b6": "o",
        "\u00c3\u00a4": "a",
    }

    for bad, good in replacements.items():
        text = text.replace(bad, good)

    return text


def load_document(path: str):
    p = Path(path)
    suffix = p.suffix.lower()

    if suffix == ".pdf":
        docs = PyPDFLoader(str(p)).load()

    elif suffix == ".docx":
        docs = Docx2txtLoader(str(p)).load()

    elif suffix in {".txt", ".md"}:
        docs = TextLoader(
            str(p),
            encoding="utf-8",
        ).load()

    else:
        raise ValueError(f"Unsupported file type: {suffix}")

    for doc in docs:
        doc.page_content = clean_text(doc.page_content)
        doc.metadata["source"] = p.name
        doc.metadata["file_type"] = suffix.lstrip(".")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )

    return splitter.split_documents(docs)