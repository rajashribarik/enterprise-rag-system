from src.evaluation import keyword_recall

def test_keyword_recall():
    assert keyword_recall("Python and FAISS", ["Python", "FAISS"]) == 1.0
