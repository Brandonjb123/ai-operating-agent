"""
Dependency untuk mendapatkan user yang sedang login dari JWT bearer token.
Menggunakan OAuth2PasswordBearer, decode token, dan mengambil user dari database.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.jwt import decode_access_token
from app.dependencies.database import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository
from jose import JWTError

# URL relatif untuk endpoint login (prefix /auth sudah ada di router)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Mendekode JWT token, memvalidasi, dan mengembalikan user yang sesuai.

    Args:
        token (str): Bearer token dari header Authorization.
        db (Session): SQLAlchemy session yang diinjeksi.

    Returns:
        User: Instance model User jika token valid.

    Raises:
        HTTPException 401: Jika token invalid, expired, atau user tidak ditemukan.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # 1. Decode token
    try:
        payload = decode_access_token(token)
    except JWTError:
        raise credentials_exception

    # 2. Ambil email (claim "sub")
    email: str | None = payload.get("sub")
    if email is None:
        raise credentials_exception

    # 3. Cari user di database
    user_repo = UserRepository(db)
    user = user_repo.get_by_email(email)
    if user is None:
        raise credentials_exception

    return user