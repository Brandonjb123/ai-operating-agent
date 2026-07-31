"""
Database dependency – menyediakan session SQLAlchemy via FastAPI Depends.
"""

from typing import Generator
from sqlalchemy.orm import Session
from app.database.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Dependency yang memberikan session database.
    Session akan otomatis ditutup setelah request selesai.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()