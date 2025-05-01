# backend/app/routes/upload.py
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from app.models import SessionLocal, Site, User
from app.routes.web import get_current_user, get_db
from services.rag_service import RAGService
from libs.rag_lib.stores.faiss_store import FAISSStore
from libs.rag_lib.chat_providers.openai_chat import OpenAIChatProvider
from app.config import settings

router = APIRouter(prefix="/api/site", tags=["api-upload"])


@router.post(
    "/{site_id}/upload",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="(API) TXT 파일 업로드 + RAG ingest",
)
async def api_upload(
    site_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 1) 사용자·사이트 권한 확인
    site = (
        db.query(Site)
        .filter(Site.id == site_id, Site.user_id == current_user.id)
        .first()
    )
    if not site:
        raise HTTPException(status_code=404, detail="Site를 찾을 수 없습니다.")
    if not file.filename.endswith(".txt"):
        raise HTTPException(
            status_code=400, detail="텍스트(.txt) 파일만 업로드 가능합니다."
        )

    # 2) 파일 읽기
    text = (await file.read()).decode("utf-8", errors="ignore")

    # 3) RAG ingest
    faiss_store = FAISSStore(
        embedding_model="text-embedding-ada-002", index_path=f"indexes/{site.site_key}"
    )
    provider = OpenAIChatProvider(api_key=settings.OPENAI_KEY)
    rag = RAGService(store=faiss_store, provider=provider, top_k=5)
    rag.ingest_documents([text])

    # 4) (선택) 문서 이력 DB에 저장하려면 여기서 crud.create_document 같은 함수를 호출

    return
