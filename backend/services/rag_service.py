# backend/services/rag_service.py

from typing import List
from libs.rag_lib.interfaces import EmbeddingStore, ChatProvider
from libs.rag_lib.stores.faiss_store import FAISSStore
from libs.rag_lib.chat_providers.openai_chat import OpenAIChatProvider
from libs.rag_lib.service import RAGService

# 1) site_id 별로 인덱스를 분리하고 싶으면 index_path 에 site_id를 포함하세요.
DEFAULT_INDEX_PATH = "faiss_index"

# RAGService 인스턴스를 전역 하나만 쓰고 싶으면 여기에 생성해 두고,
# 아니면 요청마다 새로 만드셔도 됩니다.
store: EmbeddingStore = FAISSStore(
    embedding_model="text-embedding-ada-002", index_path=DEFAULT_INDEX_PATH
)
provider: ChatProvider = OpenAIChatProvider(model_name="gpt-4o-mini")
rag = RAGService(store=store, provider=provider)


def ingest_documents(site_id: int, text: str) -> None:
    """
    웹(UI) 업로드 핸들러에서 호출됩니다.
    1) 파일 전체를 하나의 문서로 본다면 [text] 리스트로,
       아니면 쪼개서 여러 문서로 rag.ingest_documents([]) 에 넘겨도 돼요.
    2) RAGService 안에서 FAISSStore.add_documents() → 저장까지 해 줍니다.
    """
    # (선택) site_id별 인덱스를 따로 두고 싶으면 여기서 index_path를 바꿔서 store를 재생성하세요.
    documents: List[str] = [text]
    rag.ingest_documents(documents)
