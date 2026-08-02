"""
Role Repository — akses data untuk entitas Role.
Menggunakan SQLAlchemy 2.0 style, Session injection, tanpa business logic.
"""

from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.role import Role
from sqlalchemy import func


class RoleRepository:
    """
    Repository untuk entitas Role.
    Menyediakan operasi dasar CRUD dan pencarian berdasarkan organisasi.
    """

    def __init__(self, db: Session) -> None:
        """
        Inisialisasi repository dengan session database yang di-inject.

        Args:
            db (Session): SQLAlchemy Session aktif.
        """
        self.db = db

    def get_by_id(self, role_id: UUID) -> Role | None:
        """
        Mencari role berdasarkan ID.

        Args:
            role_id (UUID): UUID role.

        Returns:
            Role | None: Objek role jika ditemukan, None jika tidak.
        """
        stmt = select(Role).where(Role.id == role_id)
        return self.db.scalar(stmt)

    def get_by_name(self, organization_id: UUID, name: str) -> Role | None:
        stmt = (
            select(Role)
            .where(Role.organization_id == organization_id)
            .where(func.lower(Role.name) == name.lower())
        )
        return self.db.scalar(stmt)

    def list(
        self, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[Role]:
        """
        Mengambil daftar role dalam satu organisasi dengan paginasi.

        Args:
            organization_id (UUID): UUID organisasi.
            skip (int): Offset data.
            limit (int): Maksimum data yang dikembalikan.

        Returns:
            list[Role]: Daftar objek Role.
        """
        stmt = (
            select(Role)
            .where(Role.organization_id == organization_id)
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())

    def create(self, role: Role) -> Role:
        """
        Menyimpan role baru ke database.

        Args:
            role (Role): Objek Role yang akan disimpan.

        Returns:
            Role: Objek Role yang sudah disimpan (dengan ID terisi).
        """
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return role

    def update(self, role: Role) -> Role:
        """
        Memperbarui data role yang sudah ada.

        Args:
            role (Role): Objek Role dengan data terbaru.

        Returns:
            Role: Objek Role yang sudah diperbarui.
        """
        self.db.merge(role)
        self.db.commit()
        self.db.refresh(role)
        return role

    def delete(self, role: Role) -> None:
        """
        Menghapus role dari database.

        Args:
            role (Role): Objek Role yang akan dihapus.
        """
        self.db.delete(role)
        self.db.commit()