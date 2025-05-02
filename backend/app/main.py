# main.py: FastAPI 앱 생성, 라우터 포함, StaticFiles 설정
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.routes import auth, site, chat, upload, widget
from pathlib import Path
from fastapi.templating import Jinja2Templates
from app.routes.web import router as web_router
from app.routes.site import router as site_router
from app.models import Base, engine

# widget 폴더 (backend/widget) 로드
BASE_DIR = Path(__file__).resolve().parent.parent.parent
WIDGET_DIR = BASE_DIR / "backend" / "widget"

# frontend 정적·템플릿 경로
STATIC_DIR = BASE_DIR / "frontend" / "static"
TEMPLATES_DIR = BASE_DIR / "frontend" / "templates"

app = FastAPI()


@app.on_event("startup")
def create_tables():
    # settings.DATABASE_URL로 연결된 engine에
    # Base에 정의된 모든 모델의 테이블을 생성합니다.
    Base.metadata.create_all(bind=engine)
    # 첫 실행 시 data/dev.db 에 users, sites, documents ... 테이블이 생깁니다.


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
