# auth_service.py: 회원가입·로그인 관련 '뇌' 역할을 하는 함수들을 모아둔 파일이에요.

from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from app.config import settings

# 1) 비밀번호 해시(암호화) 알고리즘 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    평문 비밀번호를 받아서 암호화된 문자열로 바꿔줘요.
    - password: 사용자가 입력한 원래 비밀번호
    - return: 안전하게 바뀐(해시된) 비밀번호
    """
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """
    사용자가 입력한 비밀번호가, 저장된 해시와 일치하는지 확인해요.
    - plain: 사용자가 입력한 비밀번호
    - hashed: DB에 저장된 해시 비밀번호
    - return: 맞으면 True, 틀리면 False
    """
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict) -> str:
    """
    로그인 성공 후에 사용자에게 줄 '토큰'을 만들어 줘요.
    이 토큰이 있으면 다음 요청부터 '이 사람은 로그인된 상태'라고 인정해 줍니다.
    - data: 토큰 안에 담을 정보 (예: {"sub": "사용자ID"})
    - return: JWT 형식의 문자열 토큰
    """
    # 1) 토큰 만료 시간 계산 (지금부터 settings.ACCESS_TOKEN_EXPIRE_MINUTES 분 후)
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    to_encode.update({"exp": expire})  # exp 필드에 만료 시각 추가

    # 2) SECRET_KEY로 서명해서 토큰 발급
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def authenticate_user(db, email: str, password: str):
    """
    로그인 로직의 핵심!
    1) 이메일로 사용자 찾기
    2) 입력 비밀번호와 해시 비밀번호 비교
    3) 맞으면 사용자 객체, 틀리면 None 반환
    """
    from app.crud import get_user_by_email  # 순환 import 피하기 위해 함수 안에서 임포트

    user = get_user_by_email(db, email)  # 1) DB에서 사용자 조회
    if not user:
        return None  # 사용자가 없으면 실패

    if not verify_password(password, user.password):
        return None  # 비밀번호 불일치하면 실패

    return user  # 둘 다 성공하면 User 반환
