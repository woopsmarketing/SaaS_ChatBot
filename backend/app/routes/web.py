# backend/app/routes/web.py

from fastapi import APIRouter, Request, Depends, Form, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from pathlib import Path
from app.config import settings
from app.models import SessionLocal, User, Site
from app.crud import (
    get_user_by_email,
    get_user,
    create_user,
    update_site as crud_update_site,
    create_site,
    create_document,
)
from app.dependencies import get_rag_service
import uuid
from services.auth_service import verify_password, create_access_token
from services.rag_service import ingest_documents  # RAG 문서 적재 함수
from fastapi import HTTPException
from services.auth_service import hash_password
from services.rag_service import RAGService
from libs.rag_lib.stores.faiss_store import FAISSStore
from libs.rag_lib.chat_providers.openai_chat import OpenAIChatProvider
from app.config import settings  # OPENAI_KEY를 가져오기 위해

router = APIRouter()
templates = Jinja2Templates(
    directory=str(
        Path(__file__).resolve().parent.parent.parent.parent / "frontend" / "templates"
    )
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    # 1) 헤더 혹은 쿠키에서 토큰 꺼내기
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ", 1)[1]
    else:
        token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(401, "로그인이 필요합니다.")
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id = int(payload.get("sub"))
    except JWTError:
        return None
    return get_user(db, user_id)


# ──────────────────────────────────────────────
# 1) 회원가입 폼 보여주기
@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(
        "register.html", {"request": request, "error": None}
    )


# 2) 회원가입 처리
@router.post("/register", response_class=HTMLResponse)
def register(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    # 중복 확인
    if get_user_by_email(db, email):
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "이미 등록된 이메일입니다."},
            status_code=400,
        )
    # 저장
    hashed_pw = hash_password(password)
    create_user(db, email, hashed_pw)
    # 가입 후 바로 로그인 페이지로 리다이렉트
    return RedirectResponse(url="/login", status_code=302)


# 1) GET  → 빈 설정 폼 보여주기
@router.get("/site/create", response_class=HTMLResponse)
def new_site_form(request: Request, user: User = Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/login")
    # settings.html 에는 Form(action="/site/create", method="post") 가 있어야 합니다.
    return templates.TemplateResponse(
        "settings.html", {"request": request, "error": None}
    )


# 2) POST → 폼으로 넘어온 값을 받아서 DB 에 저장하고 대시보드로 되돌아가기
@router.post("/site/create", response_class=HTMLResponse)
def create_site_form(
    request: Request,
    persona_prompt: str = Form(...),  # form 필드 수신
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if not user:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")
    # site_key 는 UUID 로 발급
    site = create_site(
        db, user_id=user.id, site_key=str(uuid.uuid4()), persona_prompt=persona_prompt
    )
    # 등록 후엔 dashboard 로 돌려보낼게요
    response = RedirectResponse(url="/dashboard", status_code=302)
    return response


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})


@router.post("/login", response_class=HTMLResponse)
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.password):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "이메일 또는 비밀번호가 올바르지 않습니다."},
            status_code=401,
        )
    token = create_access_token({"sub": str(user.id)})
    response = RedirectResponse(url="/dashboard", status_code=302)
    response.set_cookie(key="access_token", value=token, httponly=True)
    return response


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not user:
        return RedirectResponse(url="/login")
    sites = db.query(Site).filter(Site.user_id == user.id).all()
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "user": user, "sites": sites}
    )


# ─── 1) 챗봇 설정 페이지 ───────────────────────────────────────────
@router.get("/site/{site_id}/settings", response_class=HTMLResponse)
def settings_page(
    request: Request,
    site_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not user:
        return RedirectResponse(url="/login")
    site = db.query(Site).filter(Site.id == site_id, Site.user_id == user.id).first()
    if not site:
        raise HTTPException(404, "해당 사이트를 찾을 수 없습니다.")
    return templates.TemplateResponse(
        "settings.html", {"request": request, "site": site}
    )


@router.post("/site/{site_id}/settings", response_class=HTMLResponse)
def settings_save(
    request: Request,
    site_id: int,
    persona_prompt: str = Form(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not user:
        return RedirectResponse(url="/login")
    # DB에 저장
    crud_update_site(db, site_id, persona_prompt)
    return RedirectResponse(url="/dashboard", status_code=302)


# ─── 2) 문서 업로드 페이지 ───────────────────────────────────────────
@router.get("/site/{site_id}/upload", response_class=HTMLResponse)
def upload_page(
    request: Request,
    site_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not user:
        return RedirectResponse(url="/login")
    site = db.query(Site).filter(Site.id == site_id, Site.user_id == user.id).first()
    if not site:
        raise HTTPException(404, "해당 사이트를 찾을 수 없습니다.")
    return templates.TemplateResponse(
        "upload.html", {"request": request, "site": site, "error": None}
    )


@router.post("/site/{site_id}/upload", response_class=HTMLResponse)
async def upload_submit(
    request: Request,
    site_id: int,
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # 1) 로그인·권한 체크
    if not user:
        return RedirectResponse(url="/login")
    site = db.query(Site).filter(Site.id == site_id, Site.user_id == user.id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site를 찾을 수 없습니다.")

    # 2) 파일 확장자 검사
    if not file.filename.endswith(".txt"):
        return templates.TemplateResponse(
            "upload.html",
            {
                "request": request,
                "site": site,
                "error": "텍스트(.txt) 파일만 업로드 가능합니다.",
            },
            status_code=400,
        )
    #    - index_path: 학습 결과(벡터 인덱스)를 저장할 폴더. site_key 별로 분리하면 좋습니다.
    try:
        
        # 3) 파일 읽어서 텍스트로 변환
        contents = await file.read()
        text = contents.decode("utf-8", errors="ignore")

        # 4) RAGService 로 학습 수행
        rag = get_rag_service(site.site_key)

        rag.ingest_documents([text])
    except Exception as e:
        return templates.TemplateResponse(
            "upload.html",
            {"request": request, "site": site, "error": f"학습 중 오류: {e}"},
            status_code=500,
        )
    create_document(db, site_id, text)
    # 5) 완료 후 대시보드로 돌려보내기
    return RedirectResponse(url="/dashboard", status_code=302)
