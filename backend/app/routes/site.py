# site.py: 사이트 등록 & 설정 엔드포인트
from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from app.crud import (
    create_site,
    get_sites_by_user,
    get_site,
    update_site as crud_update_site,
    delete_site as crud_delete_site,
)
from app.models import SessionLocal, Site, User
import uuid
from app.schemas import SiteCreate, SiteRead, SiteUpdate
from app.routes.web import get_current_user  # JWT로 인증된 User 가져오기

router = APIRouter(prefix="/site")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ──────────────────────────────────────────────────────
# 1) 내 계정의 Site 목록 조회 (JSON)
@router.get("/", response_model=list[SiteRead], summary="내가 등록한 Site 리스트 조회")
def list_sites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")
    return get_sites_by_user(db, current_user.id)


# 2) Site 상세 조회
@router.get("/{site_id}", response_model=SiteRead, summary="Site 상세 조회")
def read_site(
    site_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    site = get_site(db, site_id)
    if not site or site.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Site를 찾을 수 없습니다.")
    return site


# ──────────────────────────────────────────────────────
@router.post(
    "/",
    response_model=SiteRead,
    status_code=status.HTTP_201_CREATED,
    summary="사이트 등록 및 SiteKey 발급",
)
def register_site(
    site_in: SiteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    1) 새로운 site_key 생성
    2) create_site() 로 DB 저장
    3) 생성된 SiteRead 모델로 리턴
    """
    if not current_user:
        raise HTTPException(401, "로그인이 필요합니다.")
    site = create_site(
        db,
        user_id=current_user.id,  # TODO: 실제론 current_user.id
        site_key=str(uuid.uuid4()),
        persona_prompt=site_in.persona_prompt,  # 여기로 변경
    )
    return site


# ──────────────────────────────────────────────────────


@router.put("/{site_id}", response_model=SiteRead)
def update_site(
    site_id: int,
    site_in: SiteUpdate,  # JSON 바디로 받은 수정 데이터
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    site = get_site(db, site_id)
    if not site or site.user_id != current_user.id:
        raise HTTPException(404, "Site를 찾을 수 없습니다.")
    updated = crud_update_site(db, site_id, site_in.persona_prompt)
    return updated


# ──────────────────────────────────────────────────────


@router.delete("/{site_id}", status_code=204)
def delete_site(
    site_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    site = get_site(db, site_id)
    if not site or site.user_id != current_user.id:
        raise HTTPException(404, "Site를 찾을 수 없습니다.")
    crud_delete_site(db, site_id)
