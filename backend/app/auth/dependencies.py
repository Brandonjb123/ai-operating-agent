"""
Dependency untuk mendapatkan user yang sedang login dari JWT bearer token.
Menggunakan HTTPBearer agar Swagger menampilkan input token sederhana.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError

from app.auth.jwt import decode_access_token
from app.dependencies.database import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Mendekode JWT token dari header Authorization Bearer, validasi, dan mengembalikan user.

    Args:
        credentials: Berisi token yang diekstrak dari header.
        db: SQLAlchemy session.

    Returns:
        User: Instance model User.

    Raises:
        HTTPException 401: Jika token tidak valid atau user tidak ditemukan.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials  # string token JWT

    try:
        payload = decode_access_token(token)
    except JWTError:
        raise credentials_exception

    email: str | None = payload.get("sub")
    if email is None:
        raise credentials_exception

    user_repo = UserRepository(db)
    user = user_repo.get_by_email(email)
    if user is None:
        raise credentials_exception

    return user