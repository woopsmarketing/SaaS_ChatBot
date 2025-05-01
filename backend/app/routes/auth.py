# auth.py: 이 파일에서 '/auth/register'와 '/auth/login' 경로를 담당해요.

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import UserCreate, Token
from services.auth_service import hash_password, authenticate_user, create_access_token
from app.crud import create_user, get_user_by_email
from app.models import SessionLocal

router = APIRouter()


def get_db():
    """
    매 요청마다 DB 세션을 열고, 끝나면 닫아 주는 의존성 함수예요.
    FastAPI가 자동으로 호출해 줍니다.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", status_code=status.HTTP_201_CREATED, summary="회원가입")
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    새 사용자를 DB에 등록하는 엔드포인트입니다.
    1) 비밀번호를 hash_password로 암호화
    2) create_user로 DB 저장
    3) 이메일(id)만 리턴
    """
    # 1) 이메일 중복 방지: 이미 존재하면 400 에러
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    # 2) 비밀번호 암호화 및 생성
    hashed_pw = hash_password(user.password)
    created = create_user(db, user.email, hashed_pw)

    # 3) 결과 리턴 (보안상 비밀번호는 제외)
    return {"id": created.id, "email": created.email}


@router.post("/login", response_model=Token, summary="로그인")
def login(form_data: UserCreate, db: Session = Depends(get_db)):
    """
    사용자가 로그인할 때 호출하는 엔드포인트입니다.
    1) authenticate_user로 사용자 검증
    2) create_access_token으로 JWT 생성
    3) access_token과 token_type 반환
    """
    user = authenticate_user(db, form_data.email, form_data.password)
    if not user:
        # 인증 실패 시 401 Unauthorized 에러
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # JWT 토큰 발급
    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
