# init_db.py: DB 초기화 및 시드 데이터
import os, sys

# 이 파일 위치(backend/scripts)에서 한 단계 위(backend)를 모듈 경로에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.config import settings
from app.models import Base, engine


def init():
    Base.metadata.create_all(bind=engine)
    print("Database initialized")


if __name__ == "__main__":
    init()
