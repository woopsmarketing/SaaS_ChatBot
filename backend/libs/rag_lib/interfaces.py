from abc import ABC, abstractmethod
from typing import List, Any

class EmbeddingStore(ABC):
    @abstractmethod
    def add_documents(self, docs: List[str]) -> None:
        """문서 리스트를 받아 벡터화하고 저장"""
        pass

    @abstractmethod
    def retrieve(self, query: str, top_k: int) -> List[str]:
        """질문(query)에 유사한 문서 텍스트를 반환"""
        pass

class ChatProvider(ABC):
    @abstractmethod
    def chat(self, prompt: str, context: List[str]) -> str:
        """문맥(context)와 함께 LLM을 호출하여 답변 생성"""
        pass