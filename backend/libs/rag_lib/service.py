from typing import List
from libs.rag_lib.interfaces import EmbeddingStore, ChatProvider


class RAGService:
    def __init__(self, store: EmbeddingStore, provider: ChatProvider, top_k: int = 5):
        self.store = store
        self.provider = provider
        self.top_k = top_k

    def ingest_documents(self, documents: List[str]) -> None:
        """문서 벡터화 및 스토어 저장"""
        self.store.add_documents(documents)

    def query(self, question: str) -> str:
        """유사 문서 검색 후 LLM 호출"""
        contexts = self.store.retrieve(question, top_k=self.top_k)
        answer = self.provider.chat(question, contexts)
        return answer
