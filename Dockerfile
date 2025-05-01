# ─── 프로젝트 루트/Dockerfile ───
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# ① 컨테이너 안에서 작업 디렉터리를 /app/backend 로 설정
WORKDIR /app/backend

# ② requirements.txt(루트에 있는 거 아닌, backend/requirements.txt)를 복사해서 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ③ 나머지 코드 복사
#    이때 컨텍스트가 루트이므로 frontend/, backend/ 모두 들어오지만
#    WORKDIR 가 /app/backend 이므로 하위 app/ 모듈이 바로 보입니다.
COPY . .

# ④ 포트 열기
EXPOSE 8000

# ⑤ uvicorn 에서 'app.main' 을 탑레벨 모듈로 인식하도록
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
