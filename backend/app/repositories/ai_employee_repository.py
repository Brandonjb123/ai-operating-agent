"""
AIEmployee Repository — akses data untuk entitas AIEmployee.
Menggunakan SQLAlchemy 2.0 style, Session injection, tanpa business logic.
"""

from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ai_employee import AIEmployee


class AIEmployeeRepository:
    """
    Repository untuk entitas AIEmployee.
    Menyediakan operasi dasar CRUD dan pencarian berdasarkan organisasi.
    """

    def __init__(self, db: Session) -> None:
        """
        Inisialisasi repository dengan session database yang di-inject.

        Args:
            db (Session): SQLAlchemy Session aktif.
        """
        self.db = db

    def get_by_id(self, employee_id: UUID) -> AIEmployee | None:
        """
        Mencari AIEmployee berdasarkan ID.

        Args:
            employee_id (UUID): UUID AIEmployee.

        Returns:
            AIEmployee | None: Objek AIEmployee jika ditemukan, None jika tidak.
        """
        stmt = select(AIEmployee).where(AIEmployee.id == employee_id)
        return self.db.scalar(stmt)

    def get_by_name(self, organization_id: UUID, name: str) -> AIEmployee | None:
        """
        Mencari AIEmployee berdasarkan nama dalam satu organisasi.

        Args:
            organization_id (UUID): UUID organisasi.
            name (str): Nama AIEmployee yang dicari.

        Returns:
            AIEmployee | None: Objek AIEmployee jika ditemukan, None jika tidak.
        """
        stmt = (
            select(AIEmployee)
            .where(AIEmployee.organization_id == organization_id)
            .where(AIEmployee.name == name)
        )
        return self.db.scalar(stmt)

    def list_by_organization(
        self, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[AIEmployee]:
        """
        Mengambil daftar AIEmployee untuk satu organisasi dengan paginasi.

        Args:
            organization_id (UUID): UUID organisasi.
            skip (int): Offset data.
            limit (int): Maksimum data yang dikembalikan.

        Returns:
            list[AIEmployee]: Daftar objek AIEmployee.
        """
        stmt = (
            select(AIEmployee)
            .where(AIEmployee.organization_id == organization_id)
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())

    def create(self, employee: AIEmployee) -> AIEmployee:
        """
        Menyimpan AIEmployee baru ke database.

        Args:
            employee (AIEmployee): Objek AIEmployee yang akan disimpan.

        Returns:
            AIEmployee: Objek AIEmployee yang sudah disimpan (dengan ID terisi).
        """
        self.db.add(employee)
        self.db.commit()
        self.db.refresh(employee)
        return employee

    def update(self, employee: AIEmployee) -> AIEmployee:
        """
        Memperbarui data AIEmployee yang sudah ada.

        Args:
            employee (AIEmployee): Objek AIEmployee dengan data terbaru.

        Returns:
            AIEmployee: Objek AIEmployee yang sudah diperbarui.
        """
        self.db.merge(employee)
        self.db.commit()
        self.db.refresh(employee)
        return employee

    def delete(self, employee: AIEmployee) -> None:
        """
        Menghapus AIEmployee dari database.

        Args:
            employee (AIEmployee): Objek AIEmployee yang akan dihapus.
        """
        self.db.delete(employee)
        self.db.commit()