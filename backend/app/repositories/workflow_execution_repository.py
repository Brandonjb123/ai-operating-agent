"""
WorkflowExecution Repository — akses data untuk entitas WorkflowExecution.
Menggunakan SQLAlchemy 2.0 style, Session injection, tanpa business logic.
"""

from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.workflow_execution import WorkflowExecution


class WorkflowExecutionRepository:
    """
    Repository untuk entitas WorkflowExecution.
    Menyediakan operasi dasar CRUD dan pencarian berdasarkan workflow, AI employee, dan organisasi.
    """

    def __init__(self, db: Session) -> None:
        """
        Inisialisasi repository dengan session database yang di-inject.

        Args:
            db (Session): SQLAlchemy Session aktif.
        """
        self.db = db

    def get_by_id(self, execution_id: UUID) -> WorkflowExecution | None:
        """
        Mencari execution berdasarkan ID.

        Args:
            execution_id (UUID): UUID execution.

        Returns:
            WorkflowExecution | None: Objek WorkflowExecution jika ditemukan, None jika tidak.
        """
        stmt = select(WorkflowExecution).where(WorkflowExecution.id == execution_id)
        return self.db.scalar(stmt)

    def list_by_workflow(
        self, workflow_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[WorkflowExecution]:
        """
        Mengambil daftar execution milik satu workflow dengan paginasi.

        Args:
            workflow_id (UUID): UUID workflow.
            skip (int): Offset data.
            limit (int): Maksimum data yang dikembalikan.

        Returns:
            list[WorkflowExecution]: Daftar objek WorkflowExecution.
        """
        stmt = (
            select(WorkflowExecution)
            .where(WorkflowExecution.workflow_id == workflow_id)
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())

    def list_by_ai_employee(
        self, ai_employee_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[WorkflowExecution]:
        """
        Mengambil daftar execution milik satu AI employee dengan paginasi.

        Args:
            ai_employee_id (UUID): UUID AI employee.
            skip (int): Offset data.
            limit (int): Maksimum data yang dikembalikan.

        Returns:
            list[WorkflowExecution]: Daftar objek WorkflowExecution.
        """
        stmt = (
            select(WorkflowExecution)
            .where(WorkflowExecution.ai_employee_id == ai_employee_id)
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())

    def list_by_organization(
        self, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[WorkflowExecution]:
        """
        Mengambil daftar execution dalam satu organisasi dengan paginasi.

        Args:
            organization_id (UUID): UUID organisasi.
            skip (int): Offset data.
            limit (int): Maksimum data yang dikembalikan.

        Returns:
            list[WorkflowExecution]: Daftar objek WorkflowExecution.
        """
        stmt = (
            select(WorkflowExecution)
            .where(WorkflowExecution.organization_id == organization_id)
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())

    def create(self, execution: WorkflowExecution) -> WorkflowExecution:
        """
        Menyimpan execution baru ke database.

        Args:
            execution (WorkflowExecution): Objek WorkflowExecution yang akan disimpan.

        Returns:
            WorkflowExecution: Objek WorkflowExecution yang sudah disimpan (dengan ID terisi).
        """
        self.db.add(execution)
        self.db.commit()
        self.db.refresh(execution)
        return execution

    def update(self, execution: WorkflowExecution) -> WorkflowExecution:
        """
        Memperbarui data execution yang sudah ada.

        Args:
            execution (WorkflowExecution): Objek WorkflowExecution dengan data terbaru.

        Returns:
            WorkflowExecution: Objek WorkflowExecution yang sudah diperbarui.
        """
        self.db.merge(execution)
        self.db.commit()
        self.db.refresh(execution)
        return execution

    def delete(self, execution: WorkflowExecution) -> None:
        """
        Menghapus execution dari database.

        Args:
            execution (WorkflowExecution): Objek WorkflowExecution yang akan dihapus.
        """
        self.db.delete(execution)
        self.db.commit()