"""
Memory Repository — akses data untuk entitas Memory.
Menggunakan SQLAlchemy 2.0 style, Session injection, tanpa business logic.
"""

from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.memory import Memory


class MemoryRepository:
    """
    Repository untuk entitas Memory.
    Menyediakan operasi dasar CRUD dan pencarian berdasarkan AI employee, organisasi, dan key.
    """

    def __init__(self, db: Session) -> None:
        """
        Inisialisasi repository dengan session database yang di-inject.

        Args:
            db (Session): SQLAlchemy Session aktif.
        """
        self.db = db

    def get_by_id(self, memory_id: UUID) -> Memory | None:
        """
        Mencari memory berdasarkan ID.

        Args:
            memory_id (UUID): UUID memory.

        Returns:
            Memory | None: Objek Memory jika ditemukan, None jika tidak.
        """
        stmt = select(Memory).where(Memory.id == memory_id)
        return self.db.scalar(stmt)

    def list_by_ai_employee(
        self, ai_employee_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[Memory]:
        """
        Mengambil daftar memory milik satu AI employee dengan paginasi.

        Args:
            ai_employee_id (UUID): UUID AI employee.
            skip (int): Offset data.
            limit (int): Maksimum data yang dikembalikan.

        Returns:
            list[Memory]: Daftar objek Memory.
        """
        stmt = (
            select(Memory)
            .where(Memory.ai_employee_id == ai_employee_id)
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())

    def list_by_organization(
        self, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[Memory]:
        """
        Mengambil daftar memory dalam satu organisasi dengan paginasi.

        Args:
            organization_id (UUID): UUID organisasi.
            skip (int): Offset data.
            limit (int): Maksimum data yang dikembalikan.

        Returns:
            list[Memory]: Daftar objek Memory.
        """
        stmt = (
            select(Memory)
            .where(Memory.organization_id == organization_id)
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())

    def get_by_key(self, ai_employee_id: UUID, memory_key: str) -> Memory | None:
        """
        Mencari memory berdasarkan AI employee dan memory_key tertentu.

        Args:
            ai_employee_id (UUID): UUID AI employee.
            memory_key (str): Kunci memory yang dicari.

        Returns:
            Memory | None: Objek Memory jika ditemukan, None jika tidak.
        """
        stmt = (
            select(Memory)
            .where(Memory.ai_employee_id == ai_employee_id)
            .where(Memory.memory_key == memory_key)
        )
        return self.db.scalar(stmt)

    def create(self, memory: Memory) -> Memory:
        """
        Menyimpan memory baru ke database.

        Args:
            memory (Memory): Objek Memory yang akan disimpan.

        Returns:
            Memory: Objek Memory yang sudah disimpan (dengan ID terisi).
        """
        self.db.add(memory)
        self.db.commit()
        self.db.refresh(memory)
        return memory

    def update(self, memory: Memory) -> Memory:
        """
        Memperbarui data memory yang sudah ada.

        Args:
            memory (Memory): Objek Memory dengan data terbaru.

        Returns:
            Memory: Objek Memory yang sudah diperbarui.
        """
        self.db.merge(memory)
        self.db.commit()
        self.db.refresh(memory)
        return memory

    def delete(self, memory: Memory) -> None:
        """
        Menghapus memory dari database.

        Args:
            memory (Memory): Objek Memory yang akan dihapus.
        """
        self.db.delete(memory)
        self.db.commit()