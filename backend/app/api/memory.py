"""
Memory API router — CRUD endpoints untuk ingatan AI employee.
Prefix: /memories
Tags: Memory
"""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.repositories.memory_repository import MemoryRepository
from app.repositories.ai_employee_repository import AIEmployeeRepository
from app.services.memory_service import MemoryService
from app.schemas.memory import (
    MemoryCreateRequest,
    MemoryUpdateRequest,
    MemoryResponse,
)

router = APIRouter(prefix="/memories", tags=["Memory"])


def get_memory_service(db: Session = Depends(get_db)) -> MemoryService:
    """Dependency untuk mendapatkan instance MemoryService."""
    memory_repo = MemoryRepository(db)
    ai_employee_repo = AIEmployeeRepository(db)
    return MemoryService(memory_repo, ai_employee_repo)


@router.get("/", response_model=list[MemoryResponse])
def list_memories(
    ai_employee_id: UUID = Query(..., description="UUID AI employee pemilik memory"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    service: MemoryService = Depends(get_memory_service),
):
    """Mengambil daftar memory milik satu AI employee."""
    return service.list_memories(ai_employee_id)


@router.get("/{memory_id}", response_model=MemoryResponse)
def get_memory(
    memory_id: UUID,
    service: MemoryService = Depends(get_memory_service),
):
    """
    Mendapatkan satu memory berdasarkan ID.
    404 jika tidak ditemukan.
    """
    try:
        return service.get_memory(memory_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/", response_model=MemoryResponse, status_code=status.HTTP_201_CREATED)
def create_memory(
    request: MemoryCreateRequest,
    service: MemoryService = Depends(get_memory_service),
):
    """
    Menyimpan memory baru.
    404 jika AI employee tidak ditemukan,
    409 jika key sudah ada pada AI yang sama,
    400 untuk validasi yang gagal (importance, memory type, dll.).
    """
    try:
        return service.create_memory(request)
    except ValueError as e:
        msg = str(e).lower()
        if "ai employee not found" in msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        if "already exists" in msg:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{memory_id}", response_model=MemoryResponse)
def update_memory(
    memory_id: UUID,
    request: MemoryUpdateRequest,
    service: MemoryService = Depends(get_memory_service),
):
    """
    Memperbarui memory.
    404 jika tidak ditemukan,
    409 jika key baru bentrok,
    400 untuk validasi.
    """
    try:
        return service.update_memory(memory_id, request)
    except ValueError as e:
        msg = str(e).lower()
        if "not found" in msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        if "already exists" in msg:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{memory_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_memory(
    memory_id: UUID,
    service: MemoryService = Depends(get_memory_service),
):
    """
    Menghapus memory.
    404 jika tidak ditemukan.
    """
    try:
        service.delete_memory(memory_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))