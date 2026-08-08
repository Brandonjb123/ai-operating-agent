"""
Knowledge Repository — akses data untuk entitas Knowledge.
Menggunakan SQLAlchemy 2.0 style, Session injection, tanpa business logic.
"""

from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.knowledge import Knowledge


class KnowledgeRepository:
    """
    Repository untuk entitas Knowledge.
    Menyediakan operasi dasar CRUD dan pencarian berdasarkan AI employee, organisasi, dan judul.
    """

    def __init__(self, db: Session) -> None:
        """
        Inisialisasi repository dengan session database yang di-inject.

        Args:
            db (Session): SQLAlchemy Session aktif.
        """
        self.db = db

    def get_by_id(self, knowledge_id: UUID) -> Knowledge | None:
        """
        Mencari knowledge berdasarkan ID.

        Args:
            knowledge_id (UUID): UUID knowledge.

        Returns:
            Knowledge | None: Objek Knowledge jika ditemukan, None jika tidak.
        """
        stmt = select(Knowledge).where(Knowledge.id == knowledge_id)
        return self.db.scalar(stmt)

    def get_by_title(self, ai_employee_id: UUID, title: str) -> Knowledge | None:
        """
        Mencari knowledge berdasarkan AI employee dan judul.

        Args:
            ai_employee_id (UUID): UUID AI employee.
            title (str): Judul knowledge yang dicari.

        Returns:
            Knowledge | None: Objek Knowledge jika ditemukan, None jika tidak.
        """
        stmt = (
            select(Knowledge)
            .where(Knowledge.ai_employee_id == ai_employee_id)
            .where(Knowledge.title == title)
        )
        return self.db.scalar(stmt)

    def list_by_ai_employee(
        self, ai_employee_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[Knowledge]:
        """
        Mengambil daftar knowledge milik satu AI employee dengan paginasi.

        Args:
            ai_employee_id (UUID): UUID AI employee.
            skip (int): Offset data.
            limit (int): Maksimum data yang dikembalikan.

        Returns:
            list[Knowledge]: Daftar objek Knowledge.
        """
        stmt = (
            select(Knowledge)
            .where(Knowledge.ai_employee_id == ai_employee_id)
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())

    def list_by_organization(
        self, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[Knowledge]:
        """
        Mengambil daftar knowledge dalam satu organisasi dengan paginasi.

        Args:
            organization_id (UUID): UUID organisasi.
            skip (int): Offset data.
            limit (int): Maksimum data yang dikembalikan.

        Returns:
            list[Knowledge]: Daftar objek Knowledge.
        """
        stmt = (
            select(Knowledge)
            .where(Knowledge.organization_id == organization_id)
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())

    def create(self, knowledge: Knowledge) -> Knowledge:
        """
        Menyimpan knowledge baru ke database.

        Args:
            knowledge (Knowledge): Objek Knowledge yang akan disimpan.

        Returns:
            Knowledge: Objek Knowledge yang sudah disimpan (dengan ID terisi).
        """
        self.db.add(knowledge)
        self.db.commit()
        self.db.refresh(knowledge)
        return knowledge

    def update(self, knowledge: Knowledge) -> Knowledge:
        """
        Memperbarui data knowledge yang sudah ada.

        Args:
            knowledge (Knowledge): Objek Knowledge dengan data terbaru.

        Returns:
            Knowledge: Objek Knowledge yang sudah diperbarui.
        """
        self.db.merge(knowledge)
        self.db.commit()
        self.db.refresh(knowledge)
        return knowledge

    def delete(self, knowledge: Knowledge) -> None:
        """
        Menghapus knowledge dari database.

        Args:
            knowledge (Knowledge): Objek Knowledge yang akan dihapus.
        """
        self.db.delete(knowledge)
        self.db.commit()