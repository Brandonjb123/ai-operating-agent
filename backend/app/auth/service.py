"""
Authentication Service Layer — sudah terintegrasi dengan UserRepository,
hashing password, JWT, dan mendukung organization_id.
"""

from uuid import UUID
from sqlalchemy.orm import Session

from app.auth.security import hash_password, verify_password
from app.auth.jwt import create_access_token
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserRegisterRequest, UserLoginRequest, TokenResponse


class AuthService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.user_repository = UserRepository(db)

    def register_user(
        self, request: UserRegisterRequest, organization_id: UUID | None = None
    ) -> TokenResponse:
        if self.user_repository.exists_by_email(request.email):
            raise ValueError("Email already exists")

        hashed_password = hash_password(request.password)

        new_user = User(
            full_name=request.full_name,
            email=request.email,
            password_hash=hashed_password,
            organization_id=organization_id,
            status="active",   # ← tambahkan ini
        )

        created_user = self.user_repository.create(new_user)
        token = create_access_token(data={"sub": created_user.email})
        return TokenResponse(access_token=token, token_type="Bearer")

    def login_user(self, request: UserLoginRequest) -> TokenResponse:
        user = self.user_repository.get_by_email(request.email)
        if user is None:
            raise ValueError("Invalid email or password")

        if not verify_password(request.password, user.password_hash):
            raise ValueError("Invalid email or password")

        token = create_access_token(data={"sub": user.email})
        return TokenResponse(access_token=token, token_type="Bearer")