# backend/tests/test_auth_site.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.models import Base, engine, SessionLocal


@pytest.fixture(scope="module")
def client():
    # 테스트 전용 DB 준비 (in-memory)
    settings.DATABASE_URL = "sqlite:///:memory:"
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c


def test_register_and_login_and_site_crud(client):
    # 1) 회원가입
    res = client.post(
        "/auth/register", json={"email": "abcdefg@b.com", "password": "pass"}
    )
    assert res.status_code == 201
    user = res.json()
    assert "id" in user

    # 2) 로그인
    res = client.post(
        "/auth/login", json={"email": "abcdefg@b.com", "password": "pass"}
    )
    assert res.status_code == 200
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3) site 리스트 (아직 없음)
    res = client.get("/site/", headers=headers)
    assert res.status_code == 200 and res.json() == []

    # 4) site 생성
    res = client.post("/site/", json={"persona_prompt": "hello"}, headers=headers)
    assert res.status_code == 201
    site = res.json()
    assert site["persona_prompt"] == "hello"

    # 5) site 상세조회
    sid = site["id"]
    res = client.get(f"/site/{sid}", headers=headers)
    assert res.status_code == 200 and res.json()["id"] == sid

    # 6) site 수정
    res = client.put(f"/site/{sid}", json={"persona_prompt": "yo"}, headers=headers)
    assert res.status_code == 200 and res.json()["persona_prompt"] == "yo"

    # 7) site 삭제
    res = client.delete(f"/site/{sid}", headers=headers)
    assert res.status_code == 204
    res = client.get("/site/", headers=headers)
    assert res.json() == []
