from pathlib import Path
from src.ingestion import load_document

def test_txt_ingestion(tmp_path: Path):
    file = tmp_path / "sample.txt"
    file.write_text("AI systems retrieve information from documents.", encoding="utf-8")
    docs = load_document(str(file))
    assert docs
    assert docs[0].metadata["source"] == "sample.txt"
