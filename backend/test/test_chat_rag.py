# backend/tests/test_chat_rag.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_chat_returns_answer_field():
    res = client.post(
        "/chat",
        json={"question": "테스트 질문입니다", "site_key": "dummy"},
    )
    assert res.status_code == 200
    data = res.json()
    # answer 키가 있고, 빈 문자열이 아니어야 합니다.
    assert "answer" in data
    assert isinstance(data["answer"], str)
    assert len(data["answer"]) > 0
