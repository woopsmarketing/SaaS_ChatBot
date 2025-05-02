ARG CACHEBUST=1
# ─── 프로젝트 루트/Dockerfile ───
FROM python:3.11-slim

# (1) 표준 환경 변수
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# (2) 컨테이너 안에서 작업 디렉터리를 /app 으로 설정
WORKDIR /app

# (2.1) Python 모듈 검색 경로에 backend 폴더 추가
ENV PYTHONPATH=/app/backend \
    DATABASE_URL=sqlite:///data/dev.db

# ① 인덱스 폴더를 미리 만들어 두기
# (A) /app/indexes 폴더를 root 권한으로 생성 & 퍼미션 조정
RUN mkdir -p /app/data /app/indexes \
    && chown -R 1000:1000 /app/data /app/indexes


# (3) requirements.txt 복사 & 설치
#     → 레포 루트에 있는 requirements.txt 를 그대로 사용
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# (4) 전체 소스 복사
#     → /app/backend, /app/frontend, 등 모두 가져옴
COPY . .

# (5) FastAPI 포트 오픈
EXPOSE 8000

# (6) uvicorn 을 'backend.app.main' 모듈로 실행
#     → 컨텍스트(/app) 아래에 backend/app/main.py 가 있으므로
CMD ["uvicorn", "backend.app.main:app",
     "--host", "0.0.0.0", "--port", "8000",
     "--log-level", "warning"]
