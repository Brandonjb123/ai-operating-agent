"""
Organization Repository — akses data untuk entitas Organization.
Menggunakan SQLAlchemy 2.0 style, Session injection, tanpa business logic.
"""

from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.organization import Organization


class OrganizationRepository:
    """
    Repository untuk entitas Organization.
    Menyediakan operasi dasar CRUD dan pencarian.
    """

    def __init__(self, db: Session) -> None:
        """
        Inisialisasi repository dengan session database yang di-inject.

        Args:
            db (Session): SQLAlchemy Session aktif.
        """
        self.db = db

    def get_by_id(self, organization_id: UUID) -> Organization | None:
        """
        Mencari organisasi berdasarkan ID.

        Args:
            organization_id (UUID): UUID organisasi.

        Returns:
            Organization | None: Objek organisasi jika ditemukan, None jika tidak.
        """
        stmt = select(Organization).where(Organization.id == organization_id)
        return self.db.scalar(stmt)

    def get_by_slug(self, slug: str) -> Organization | None:
        """
        Mencari organisasi berdasarkan slug unik.

        Args:
            slug (str): Slug organisasi.

        Returns:
            Organization | None: Objek organisasi jika ditemukan, None jika tidak.
        """
        stmt = select(Organization).where(Organization.slug == slug)
        return self.db.scalar(stmt)

    def list(self, skip: int = 0, limit: int = 100) -> list[Organization]:
        """
        Mengambil daftar organisasi dengan paginasi.

        Args:
            skip (int): Jumlah data yang dilewati (offset).
            limit (int): Maksimum jumlah data yang dikembalikan.

        Returns:
            list[Organization]: Daftar objek Organization.
        """
        stmt = select(Organization).offset(skip).limit(limit)
        return list(self.db.scalars(stmt).all())

    def create(self, organization: Organization) -> Organization:
        """
        Menyimpan organisasi baru ke database.

        Args:
            organization (Organization): Objek Organization yang akan disimpan.

        Returns:
            Organization: Objek Organization yang sudah disimpan (dengan ID terisi).
        """
        self.db.add(organization)
        self.db.commit()
        self.db.refresh(organization)
        return organization

    def update(self, organization: Organization) -> Organization:
        """
        Memperbarui data organisasi yang sudah ada.

        Args:
            organization (Organization): Objek Organization dengan data terbaru.

        Returns:
            Organization: Objek Organization yang sudah diperbarui.
        """
        self.db.merge(organization)
        self.db.commit()
        self.db.refresh(organization)
        return organization

    def delete(self, organization: Organization) -> None:
        """
        Menghapus organisasi dari database.

        Args:
            organization (Organization): Objek Organization yang akan dihapus.
        """
        self.db.delete(organization)
        self.db.commit()