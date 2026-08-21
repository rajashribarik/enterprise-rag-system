from src.vectorstore import load_index
from src.reranker import Reranker
from src.generator import Generator
from src.config import settings

class RAGPipeline:
    def __init__(self):
        self.store = load_index()
        self.reranker = Reranker()
        self.generator = Generator()

    def answer(self, question: str):
        retrieved = self.store.similarity_search(question, k=settings.top_k)
        ranked = self.reranker.rerank(question, retrieved, settings.rerank_top_k)
        answer = self.generator.generate(question, ranked)
        sources = [
            {
                "source": d.metadata.get("source"),
                "page": d.metadata.get("page"),
                "score": score,
                "content": d.page_content[:500],
            }
            for d, score in ranked
        ]
        return {"answer": answer, "sources": sources}
