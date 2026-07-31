"""
Authentication API router.
Endpoint: /auth/register, /auth/login, /auth/me.
Menangkap ValueError dari service dan mengubah menjadi HTTPException.
"""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.organization import get_default_organization_id
from app.auth.service import AuthService
from app.auth.dependencies import get_current_user
from app.schemas.auth import UserRegisterRequest, UserLoginRequest, TokenResponse
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=201)
def register(
    request: UserRegisterRequest,
    db: Session = Depends(get_db),
    org_id: UUID = Depends(get_default_organization_id),
):
    """Mendaftarkan pengguna baru."""
    auth_service = AuthService(db)
    try:
        return auth_service.register_user(request, organization_id=org_id)
    except ValueError as e:
        if "already exists" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists",
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/login", response_model=TokenResponse)
def login(
    request: UserLoginRequest,
    db: Session = Depends(get_db),
):
    """Login dan dapatkan JWT token."""
    auth_service = AuthService(db)
    try:
        return auth_service.login_user(request)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    """Mengembalikan data pengguna yang sedang login."""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "status": current_user.status,
    }