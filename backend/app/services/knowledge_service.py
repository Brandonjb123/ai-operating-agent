"""
Knowledge Service — logika bisnis untuk manajemen pengetahuan AI employee.
Menggunakan KnowledgeRepository & AIEmployeeRepository.
"""

from uuid import UUID
from sqlalchemy.orm import Session

from app.models.knowledge import Knowledge
from app.repositories.knowledge_repository import KnowledgeRepository
from app.repositories.ai_employee_repository import AIEmployeeRepository
from app.schemas.knowledge import (
    KnowledgeCreateRequest,
    KnowledgeUpdateRequest,
    KnowledgeResponse,
    ALLOWED_KNOWLEDGE_TYPES,
    ALLOWED_STATUSES,
)


class KnowledgeService:
    """Service untuk mengelola knowledge."""

    def __init__(self, db: Session) -> None:
        """
        Inisialisasi service dengan session database.
        Repository dibuat dari session ini.
        """
        self.knowledge_repo = KnowledgeRepository(db)
        self.ai_employee_repo = AIEmployeeRepository(db)

    def list_knowledges(self, ai_employee_id: UUID) -> list[KnowledgeResponse]:
        """Mendaftar semua knowledge milik AI employee tertentu."""
        knowledges = self.knowledge_repo.list_by_ai_employee(ai_employee_id)
        return [KnowledgeResponse.model_validate(k) for k in knowledges]

    def get_knowledge(self, knowledge_id: UUID) -> KnowledgeResponse:
        """Mendapatkan knowledge berdasarkan ID."""
        knowledge = self.knowledge_repo.get_by_id(knowledge_id)
        if knowledge is None:
            raise ValueError("Knowledge not found")
        return KnowledgeResponse.model_validate(knowledge)

    def create_knowledge(self, request: KnowledgeCreateRequest) -> KnowledgeResponse:
        """Membuat knowledge baru dengan berbagai aturan bisnis."""
        # 1. Pastikan AI employee ada
        ai_employee = self.ai_employee_repo.get_by_id(request.ai_employee_id)
        if ai_employee is None:
            raise ValueError("AI employee not found")

        # 2. Validasi title
        title = request.title.strip()
        if not title:
            raise ValueError("Knowledge title is required")

        # 3. Validasi content
        content = request.content.strip()
        if not content:
            raise ValueError("Content is required")

        # 4. Cek duplikasi title dalam AI employee yang sama
        existing = self.knowledge_repo.get_by_title(request.ai_employee_id, title)
        if existing:
            raise ValueError("Knowledge with this title already exists for this AI employee")

        # 5. Validasi knowledge_type
        if request.knowledge_type.lower() not in ALLOWED_KNOWLEDGE_TYPES:
            raise ValueError(f"Unsupported knowledge type '{request.knowledge_type}'")

        # 6. Validasi status
        if request.status.lower() not in ALLOWED_STATUSES:
            raise ValueError(f"Invalid status '{request.status}'")

        # 7. Source wajib
        source = request.source.strip()
        if not source:
            raise ValueError("Source is required")

        # Buat objek Knowledge
        knowledge = Knowledge(
            organization_id=ai_employee.organization_id,
            ai_employee_id=request.ai_employee_id,
            title=title,
            content=content,
            source=source,
            knowledge_type=request.knowledge_type.lower(),
            status=request.status.lower(),
            metadata_=request.metadata_,
        )
        saved = self.knowledge_repo.create(knowledge)
        return KnowledgeResponse.model_validate(saved)

    def update_knowledge(
        self, knowledge_id: UUID, request: KnowledgeUpdateRequest
    ) -> KnowledgeResponse:
        """Memperbarui knowledge. Hanya field yang tidak None yang diupdate."""
        knowledge = self.knowledge_repo.get_by_id(knowledge_id)
        if knowledge is None:
            raise ValueError("Knowledge not found")

        # Update title
        if request.title is not None:
            new_title = request.title.strip()
            if not new_title:
                raise ValueError("Knowledge title is required")
            # Cek duplikasi title di AI employee yang sama (selain dirinya)
            existing = self.knowledge_repo.get_by_title(knowledge.ai_employee_id, new_title)
            if existing and existing.id != knowledge_id:
                raise ValueError("Knowledge with this title already exists for this AI employee")
            knowledge.title = new_title

        # Update content
        if request.content is not None:
            content = request.content.strip()
            if not content:
                raise ValueError("Content is required")
            knowledge.content = content

        # Update source
        if request.source is not None:
            source = request.source.strip()
            if not source:
                raise ValueError("Source is required")
            knowledge.source = source

        # Update knowledge_type
        if request.knowledge_type is not None:
            if request.knowledge_type.lower() not in ALLOWED_KNOWLEDGE_TYPES:
                raise ValueError(f"Unsupported knowledge type '{request.knowledge_type}'")
            knowledge.knowledge_type = request.knowledge_type.lower()

        # Update status
        if request.status is not None:
            if request.status.lower() not in ALLOWED_STATUSES:
                raise ValueError(f"Invalid status '{request.status}'")
            knowledge.status = request.status.lower()

        # Update metadata
        if request.metadata_ is not None:
            knowledge.metadata_ = request.metadata_

        updated = self.knowledge_repo.update(knowledge)
        return KnowledgeResponse.model_validate(updated)

    def delete_knowledge(self, knowledge_id: UUID) -> None:
        """Menghapus knowledge berdasarkan ID."""
        knowledge = self.knowledge_repo.get_by_id(knowledge_id)
        if knowledge is None:
            raise ValueError("Knowledge not found")
        self.knowledge_repo.delete(knowledge)