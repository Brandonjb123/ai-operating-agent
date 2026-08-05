"""
Memory Service — logika bisnis untuk manajemen ingatan AI employee.
Menggunakan MemoryRepository & AIEmployeeRepository.
"""

from uuid import UUID
from datetime import datetime, timezone

from app.models.memory import Memory
from app.repositories.memory_repository import MemoryRepository
from app.repositories.ai_employee_repository import AIEmployeeRepository
from app.schemas.memory import (
    MemoryCreateRequest,
    MemoryUpdateRequest,
    MemoryResponse,
    ALLOWED_MEMORY_TYPES,
)


class MemoryService:
    """Service untuk mengelola ingatan AI."""

    def __init__(
        self,
        memory_repo: MemoryRepository,
        ai_employee_repo: AIEmployeeRepository,
    ) -> None:
        self.memory_repo = memory_repo
        self.ai_employee_repo = ai_employee_repo

    def list_memories(self, ai_employee_id: UUID) -> list[MemoryResponse]:
        """Mendaftar semua memory milik AI employee tertentu."""
        memories = self.memory_repo.list_by_ai_employee(ai_employee_id)
        return [MemoryResponse.model_validate(m) for m in memories]

    def get_memory(self, memory_id: UUID) -> MemoryResponse:
        """
        Mendapatkan memory berdasarkan ID.
        Otomatis memperbarui last_accessed_at ke waktu saat ini.
        """
        memory = self.memory_repo.get_by_id(memory_id)
        if memory is None:
            raise ValueError("Memory not found")

        # Perbarui last_accessed_at
        memory.last_accessed_at = datetime.now(timezone.utc)
        self.memory_repo.update(memory)

        return MemoryResponse.model_validate(memory)

    def create_memory(self, request: MemoryCreateRequest) -> MemoryResponse:
        """Menyimpan memory baru dengan berbagai validasi bisnis."""
        # 1. Pastikan AI employee ada
        ai_employee = self.ai_employee_repo.get_by_id(request.ai_employee_id)
        if ai_employee is None:
            raise ValueError("AI employee not found")

        # 2. memory_key tidak boleh kosong (sudah divalidasi schema, tapi double-check)
        key = request.memory_key.strip()
        if not key:
            raise ValueError("Memory key is required")

        # 3. memory_value tidak boleh kosong
        value = request.memory_value.strip()
        if not value:
            raise ValueError("Memory value is required")

        # 4. Cek duplikasi key pada AI yang sama
        existing = self.memory_repo.get_by_key(request.ai_employee_id, key)
        if existing:
            raise ValueError("Memory with this key already exists for this AI employee")

        # 5. Validasi memory_type (sudah di schema)
        if request.memory_type.lower() not in ALLOWED_MEMORY_TYPES:
            raise ValueError(f"Unsupported memory type '{request.memory_type}'")

        # 6. Validasi importance (sudah di schema, tambahan)
        if not (1 <= request.importance <= 10):
            raise ValueError("Importance must be between 1 and 10")

        # Buat objek Memory
        memory = Memory(
            organization_id=ai_employee.organization_id,
            ai_employee_id=request.ai_employee_id,
            memory_key=key,
            memory_value=value,
            memory_type=request.memory_type.lower(),
            importance=request.importance,
            metadata_=request.metadata_,
            last_accessed_at=datetime.now(timezone.utc),
        )
        saved = self.memory_repo.create(memory)
        return MemoryResponse.model_validate(saved)

    def update_memory(
        self, memory_id: UUID, request: MemoryUpdateRequest
    ) -> MemoryResponse:
        """Memperbarui memory. Hanya field yang tidak None yang diupdate."""
        memory = self.memory_repo.get_by_id(memory_id)
        if memory is None:
            raise ValueError("Memory not found")

        # Update memory_key (jika diberikan)
        if request.memory_key is not None:
            new_key = request.memory_key.strip()
            if not new_key:
                raise ValueError("Memory key is required")
            # Cek duplikasi key dengan AI employee yang sama (selain dirinya)
            existing = self.memory_repo.get_by_key(memory.ai_employee_id, new_key)
            if existing and existing.id != memory_id:
                raise ValueError("Memory with this key already exists for this AI employee")
            memory.memory_key = new_key

        # Update memory_value
        if request.memory_value is not None:
            val = request.memory_value.strip()
            if not val:
                raise ValueError("Memory value is required")
            memory.memory_value = val

        # Update memory_type
        if request.memory_type is not None:
            if request.memory_type.lower() not in ALLOWED_MEMORY_TYPES:
                raise ValueError(f"Unsupported memory type '{request.memory_type}'")
            memory.memory_type = request.memory_type.lower()

        # Update importance
        if request.importance is not None:
            if not (1 <= request.importance <= 10):
                raise ValueError("Importance must be between 1 and 10")
            memory.importance = request.importance

        # Update metadata
        if request.metadata_ is not None:
            memory.metadata_ = request.metadata_

        updated = self.memory_repo.update(memory)
        return MemoryResponse.model_validate(updated)

    def delete_memory(self, memory_id: UUID) -> None:
        """Menghapus memory berdasarkan ID."""
        memory = self.memory_repo.get_by_id(memory_id)
        if memory is None:
            raise ValueError("Memory not found")
        self.memory_repo.delete(memory)