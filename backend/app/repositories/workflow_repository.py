"""
Workflow Repository — akses data untuk entitas Workflow.
Menggunakan SQLAlchemy 2.0 style, Session injection, tanpa business logic.
"""

from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.workflow import Workflow


class WorkflowRepository:
    """
    Repository untuk entitas Workflow.
    Menyediakan operasi dasar CRUD dan pencarian berdasarkan AI employee, organisasi, dan nama.
    """

    def __init__(self, db: Session) -> None:
        """
        Inisialisasi repository dengan session database yang di-inject.

        Args:
            db (Session): SQLAlchemy Session aktif.
        """
        self.db = db

    def get_by_id(self, workflow_id: UUID) -> Workflow | None:
        """
        Mencari workflow berdasarkan ID.

        Args:
            workflow_id (UUID): UUID workflow.

        Returns:
            Workflow | None: Objek Workflow jika ditemukan, None jika tidak.
        """
        stmt = select(Workflow).where(Workflow.id == workflow_id)
        return self.db.scalar(stmt)

    def get_by_name(self, ai_employee_id: UUID, name: str) -> Workflow | None:
        """
        Mencari workflow berdasarkan AI employee dan nama.

        Args:
            ai_employee_id (UUID): UUID AI employee.
            name (str): Nama workflow yang dicari.

        Returns:
            Workflow | None: Objek Workflow jika ditemukan, None jika tidak.
        """
        stmt = (
            select(Workflow)
            .where(Workflow.ai_employee_id == ai_employee_id)
            .where(Workflow.name == name)
        )
        return self.db.scalar(stmt)

    def list_by_ai_employee(
        self, ai_employee_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[Workflow]:
        """
        Mengambil daftar workflow milik satu AI employee dengan paginasi.

        Args:
            ai_employee_id (UUID): UUID AI employee.
            skip (int): Offset data.
            limit (int): Maksimum data yang dikembalikan.

        Returns:
            list[Workflow]: Daftar objek Workflow.
        """
        stmt = (
            select(Workflow)
            .where(Workflow.ai_employee_id == ai_employee_id)
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())

    def list_by_organization(
        self, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[Workflow]:
        """
        Mengambil daftar workflow dalam satu organisasi dengan paginasi.

        Args:
            organization_id (UUID): UUID organisasi.
            skip (int): Offset data.
            limit (int): Maksimum data yang dikembalikan.

        Returns:
            list[Workflow]: Daftar objek Workflow.
        """
        stmt = (
            select(Workflow)
            .where(Workflow.organization_id == organization_id)
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())

    def create(self, workflow: Workflow) -> Workflow:
        """
        Menyimpan workflow baru ke database.

        Args:
            workflow (Workflow): Objek Workflow yang akan disimpan.

        Returns:
            Workflow: Objek Workflow yang sudah disimpan (dengan ID terisi).
        """
        self.db.add(workflow)
        self.db.commit()
        self.db.refresh(workflow)
        return workflow

    def update(self, workflow: Workflow) -> Workflow:
        """
        Memperbarui data workflow yang sudah ada.

        Args:
            workflow (Workflow): Objek Workflow dengan data terbaru.

        Returns:
            Workflow: Objek Workflow yang sudah diperbarui.
        """
        self.db.merge(workflow)
        self.db.commit()
        self.db.refresh(workflow)
        return workflow

    def delete(self, workflow: Workflow) -> None:
        """
        Menghapus workflow dari database.

        Args:
            workflow (Workflow): Objek Workflow yang akan dihapus.
        """
        self.db.delete(workflow)
        self.db.commit()