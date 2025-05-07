# crud.py: DB CRUD 헬퍼 함수
from sqlalchemy.orm import Session
from app.models import User, Site, Chat, Document
import uuid


def get_user_by_email(db: Session, email: str) -> User | None:
    """
    이메일로 사용자 조회
    """
    return db.query(User).filter(User.email == email).first()


def get_user(db: Session, user_id: int) -> User | None:
    """
    ID로 사용자 조회
    """
    return db.get(User, user_id)


def create_user(db: Session, email: str, hashed_password: str) -> User:
    """
    새 사용자 생성
    """
    # 만약 실제 해시 처리를 여기서 하고 싶다면:

    user = User(email=email, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_site(db: Session, user_id: int, site_key: str, persona_prompt: str) -> Site:
    """
    새 사이트(챗봇 인스턴스) 생성
    """
    site = Site(user_id=user_id, site_key=site_key, persona_prompt=persona_prompt)
    db.add(site)
    db.commit()
    db.refresh(site)
    return site


def update_site(db: Session, site_id: int, new_prompt: str) -> Site:
    s = db.query(Site).filter(Site.id == site_id).first()
    s.persona_prompt = new_prompt
    db.commit()
    db.refresh(s)
    return s


def delete_site(db: Session, site_id: int):
    db.query(Site).filter(Site.id == site_id).delete()
    db.commit()


def save_chat(db: Session, site_id: int, question: str, answer: str) -> Chat:
    """
    사용자가 챗봇에 물어본 질문(question)과
    챗봇이 응답(answer)을 Chats 테이블에 저장하고
    저장된 Chat 객체를 리턴합니다.
    """
    chat = Chat(site_id=site_id, question=question, answer=answer)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat


def get_sites_by_user(db: Session, user_id: int) -> list[Site]:
    """user_id가 만든 모든 Site 반환"""
    return db.query(Site).filter(Site.user_id == user_id).all()


def get_site_by_key(db: Session, site_key: str) -> Site | None:
    """site_key로 Site 한 건 조회"""
    return db.query(Site).filter(Site.site_key == site_key).first()


def get_site(db: Session, site_id: int) -> Site | None:
    """site_id 로 Site 1개만 반환"""
    return db.query(Site).filter(Site.id == site_id).first()


def create_document(db: Session, site_id: int, content: str) -> Document:
    doc = Document(id=str(uuid.uuid4()), site_id=site_id, content=content)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc
