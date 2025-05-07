# main.py: FastAPI 앱 생성, 라우터 포함, StaticFiles 설정
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import auth, site, chat, upload, widget
from pathlib import Path
from fastapi.templating import Jinja2Templates
from app.routes.web import router as web_router
from app.routes.site import router as site_router
from app.models import Base, engine, User, Site
from app.models import SessionLocal
from app.crud import get_user_by_email

# widget 폴더 (backend/widget) 로드
BASE_DIR = Path(__file__).resolve().parent.parent.parent
WIDGET_DIR = BASE_DIR / "backend" / "widget"

# frontend 정적·템플릿 경로
STATIC_DIR = BASE_DIR / "frontend" / "static"
TEMPLATES_DIR = BASE_DIR / "frontend" / "templates"

app = FastAPI()

# 모든 도메인에 대해 CORS 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ← 여기
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def create_tables():
    # 1) 테이블 생성
    Base.metadata.create_all(bind=engine)

    # 2) 기본 계정/사이트 시딩
    db = SessionLocal()
    try:
        # --- 기본 관리자 계정 ---
        admin = get_user_by_email(db, settings.DEFAULT_ADMIN_EMAIL)
        if not admin:
            from app.crud import create_user  # your 기존 crud 함수 재사용

            admin = create_user(
                db,
                email=settings.DEFAULT_ADMIN_EMAIL,
                password=settings.DEFAULT_ADMIN_PASSWORD,  # 내부에서 해시 처리
            )
            print(f"시딩: 기본 관리자 '{settings.DEFAULT_ADMIN_EMAIL}' 생성")

        # --- 기본 사이트 (site_key) ---
        if not db.query(Site).filter_by(site_key=settings.DEFAULT_SITE_KEY).first():
            default_site = Site(
                name="Default Site",
                site_key=settings.DEFAULT_SITE_KEY,
                owner_id=admin.id,
            )
            db.add(default_site)
            db.commit()
            print(f"시딩: 기본 사이트 '{settings.DEFAULT_SITE_KEY}' 생성")
    finally:
        db.close()


# ✅ 올바른 절대경로로 마운트
app.mount("/widget", StaticFiles(directory=str(WIDGET_DIR), html=True), name="widget")

# 2) 관리자용 정적 파일 서빙 설정!
#    /static 경로로 요청이 오면 'frontend/static' 폴더를 뒤져서 파일을 응답합니다.
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


# 관리자 웹 라우터를 제일 먼저 등록
app.include_router(web_router)
# API 라우터들
app.include_router(auth.router, prefix="/auth")
app.include_router(site.router, prefix="/site")
app.include_router(chat.router, prefix="/chat")
app.include_router(upload.router, prefix="/site")
app.include_router(widget.router, prefix="/widget")
app.include_router(site_router)


@app.get("/ping")
def ping():
    return {"ok": True}
