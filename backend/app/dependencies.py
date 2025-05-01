# backend/app/dependencies.py

import os
from functools import lru_cache
from libs.rag_lib.chat_providers.openai_chat import OpenAIChatProvider
from libs.rag_lib.stores.faiss_store import FAISSStore
from services.rag_service import RAGService
from app.config import settings


# 1. LLM 프로바이더: 애플리케이션 시작 시 한 번만 생성
@lru_cache()
def get_llm_provider() -> OpenAIChatProvider:
    os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
    return OpenAIChatProvider(api_key=settings.OPENAI_API_KEY)


# 2. FAISS 스토어: site_key 별로 한 번만 로드하거나 생성
@lru_cache()
def get_faiss_store(site_key: str) -> FAISSStore:
    return FAISSStore(
        embedding_model="text-embedding-ada-002", index_path=f"indexes/{site_key}"
    )


# 3. RAG 서비스: 위 두 리소스를 묶어서 site_key 별로 한 번만 생성
@lru_cache()
def get_rag_service(site_key: str) -> RAGService:
    store = get_faiss_store(site_key)
    provider = get_llm_provider()
    return RAGService(store=store, provider=provider, top_k=5)
