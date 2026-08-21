from sentence_transformers import CrossEncoder
from src.config import settings

class Reranker:
    def __init__(self):
        self.model = CrossEncoder(settings.reranker_model)

    def rerank(self, query, documents, top_n):
        if not documents:
            return []
        pairs = [(query, d.page_content) for d in documents]
        scores = self.model.predict(pairs)
        ranked = sorted(zip(documents, scores), key=lambda x: float(x[1]), reverse=True)
        return [(doc, float(score)) for doc, score in ranked[:top_n]]
