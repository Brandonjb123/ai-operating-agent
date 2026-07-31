"""
Authentication API router.
Hanya bertugas menerima request, memanggil AuthService, dan mengembalikan response.
Tidak ada business logic di sini.
"""

from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.organization import get_default_organization_id
from app.auth.service import AuthService
from app.schemas.auth import UserRegisterRequest, UserLoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=201)
def register(
    request: UserRegisterRequest,
    db: Session = Depends(get_db),
    org_id: UUID = Depends(get_default_organization_id),
):
    """
    Mendaftarkan pengguna baru.
    """
    auth_service = AuthService(db)
    return auth_service.register_user(request, organization_id=org_id)


@router.post("/login", response_model=TokenResponse)
def login(
    request: UserLoginRequest,
    db: Session = Depends(get_db),
):
    """
    Melakukan login dan mengembalikan JWT token.
    """
    auth_service = AuthService(db)
    return auth_service.login_user(request)