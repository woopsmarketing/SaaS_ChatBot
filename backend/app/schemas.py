# schemas.py: Pydantic 요청/응답 모델
from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class SiteCreate(BaseModel):
    persona_prompt: str


class SiteUpdate(BaseModel):
    persona_prompt: str


class SiteRead(BaseModel):
    id: int
    site_key: str
    persona_prompt: str
    model_config = {"from_attributes": True}  # SQLAlchemy 모델과 매핑
    # class Config:
    #     orm_mode = True


class ChatRequest(BaseModel):
    question: str
    site_key: str


class ChatResponse(BaseModel):
    answer: str


class UserRead(BaseModel):
    id: int
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}
