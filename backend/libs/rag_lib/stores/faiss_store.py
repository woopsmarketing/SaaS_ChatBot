import os
from typing import List
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from libs.rag_lib.interfaces import EmbeddingStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.config import settings


class FAISSStore(EmbeddingStore):
    def __init__(
        self,
        embedding_model: str = "text-embedding-ada-002",
        index_path: str = "/app/indexes/faiss_index",
    ):
        os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        self.index_path = index_path
        # 1) 인덱스 폴더가 없으면 생성
        os.makedirs(self.index_path, exist_ok=True)
        # 기존에 저장된 인덱스 파일이 있는지 체크
        index_file = os.path.join(self.index_path, "index.faiss")
        # try:
        # 기존 인덱스가 있으면 로드

        if os.path.exists(index_file):
            # 있으면 로드
            self.store = FAISS.load_local(
                self.index_path, self.embeddings, allow_dangerous_deserialization=True
            )
        else:
            # 없으면 나중에 add_documents() 에서 생성
            self.store = None
        # except Exception as e:
        #     # ★ 개발 중에는 에러 무시하고 넘어가세요.
        #     #    실제 RAG를 구현할 때는 여기를 적절히 채워 주시면 됩니다.
        #     print(f"[WARNING] FAISS 초기화 실패, 벡터 스토어 없이 동작합니다: {e}")

        #     # 초기화에 실패하면 dummy 스토어 만들어 두기
        #     class DummyStore:
        #         def add_documents(self, docs):
        #             pass

        #         def similarity_search(self, query, k):
        #             return []

        #         def save_local(self, path):
        #             # 저장 동작이 필요한 코드가 호출되어도 아무일도 안 일어나도록 합니다.
        #             pass

        #     self.store = DummyStore()
        #     # 새 인덱스 생성: 빈 문서 리스트로부터
        #     # self.store = FAISS.from_documents([], self.embeddings)
        #     # (빈 인덱스를 만든 뒤 나중에 add_documents 하면 됩니다)
        #     # os.makedirs(self.index_path, exist_ok=True)
        #     # self.store.save_local(self.index_path)
        #     # self.store = None

    def add_documents(self, docs: List[str]) -> None:
        splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=30)
        texts = splitter.split_text("\n\n".join(docs))

        # (2) 최초 인덱스 생성 또는 기존 인덱스에 추가
        if self.store is None:
            # 문서 리스트로부터 새로운 인덱스 생성
            self.store = FAISS.from_texts(texts, self.embeddings)
        else:
            # 이미 만들어진 인덱스가 있으면 텍스트 추가
            self.store.add_texts(texts)

        # (3) 로컬에 저장
        self.store.save_local(self.index_path)

    def retrieve(self, query: str, top_k: int = 5) -> List[str]:
        results = self.store.similarity_search(query, k=top_k)
        return [doc.page_content for doc in results]
