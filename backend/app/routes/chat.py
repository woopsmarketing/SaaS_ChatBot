# chat.py: 위젯 연동 챗 엔드포인트
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import save_chat, get_site_by_key
from app.schemas import ChatRequest, ChatResponse
from app.models import SessionLocal
from app.dependencies import get_rag_service
# === 여기에 rag_lib import 추가 ===
from libs.rag_lib.stores.faiss_store import FAISSStore
from libs.rag_lib.chat_providers.openai_chat import OpenAIChatProvider
from libs.rag_lib.service import RAGService

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ChatResponse)
@router.post("", response_model=ChatResponse)
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    # 임시 답변
    # answer = "This is a stub"
    # 1) RAGService 인스턴스 생성 (모듈 레벨에 한 번만 해도 됩니다)
    # 1) site_key 검증(optional)
    site = get_site_by_key(db, req.site_key)
    if not site:
        raise HTTPException(404, "존재하지 않는 site_key 입니다.")
    rag = get_rag_service(req.site_key)
    # (선택) 매 요청마다 문서를 ingest 하고 싶다면:
    # rag.ingest_documents([...])
    # 2) 실제 질문을 RAGService에 넘겨 답변 생성
    # 벡터 스토어가 없다면 바로 LLM 호출
    answer = rag.query(req.question)
    save_chat(db, site_id=site.id, question=req.question, answer=answer)
    return ChatResponse(answer=answer)
