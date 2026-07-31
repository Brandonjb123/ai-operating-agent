"""
User Repository — bertanggung jawab hanya untuk akses data pengguna ke database.
Menggunakan SQLAlchemy 2.0 style dengan Session injection.
Tidak mengandung business logic, hashing password, atau JWT.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User  # asumsikan model User berada di sini


class UserRepository:
    """
    Repository untuk entitas User.
    Menyediakan operasi dasar: cari berdasarkan email, cek keberadaan, dan buat user baru.
    Semua operasi menggunakan Session yang di-inject dari luar.
    """

    def __init__(self, db: Session) -> None:
        """
        Inisialisasi repository dengan session database.

        Args:
            db (Session): SQLAlchemy Session yang aktif (biasanya dari dependency FastAPI).
        """
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        """
        Mencari user berdasarkan email.

        Args:
            email (str): Alamat email yang dicari.

        Returns:
            User | None: Objek User jika ditemukan, None jika tidak.
        """
        stmt = select(User).where(User.email == email)
        return self.db.scalar(stmt)

    def exists_by_email(self, email: str) -> bool:
        """
        Mengecek apakah user dengan email tertentu sudah ada.

        Args:
            email (str): Alamat email yang dicek.

        Returns:
            bool: True jika email sudah terdaftar, False jika belum.
        """
        user = self.get_by_email(email)
        return user is not None

    def create(self, user: User) -> User:
        """
        Menyimpan user baru ke database.

        Args:
            user (User): Objek User yang sudah lengkap (termasuk password yang sudah di-hash).

        Returns:
            User: Objek User yang sudah disimpan (dengan ID yang di-generate database).
        """
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user