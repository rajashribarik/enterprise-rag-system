import sys
from src.ingestion import load_document
from src.vectorstore import build_index

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/index_document.py path/to/document.pdf")
    docs = load_document(sys.argv[1])
    build_index(docs)
    print(f"Indexed {len(docs)} chunks.")
