# backend/app/models.py
# import os, sys

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
from datetime import datetime

Base = declarative_base()
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Site(Base):
    __tablename__ = "sites"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    site_key = Column(String, unique=True, index=True, nullable=False)
    persona_prompt = Column(String, default="You are a friendly assistant.")


class Document(Base):
    __tablename__ = "documents"
    id = Column(String, primary_key=True)
    site_id = Column(Integer, ForeignKey("sites.id"))
    content = Column(String)


class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("sites.id"))
    question = Column(String)
    answer = Column(String)
