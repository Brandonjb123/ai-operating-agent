"""
Knowledge API router — CRUD endpoints untuk knowledge base AI employee.
Prefix: /knowledges
Tag: Knowledge
"""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.services.knowledge_service import KnowledgeService
from app.schemas.knowledge import (
    KnowledgeCreateRequest,
    KnowledgeUpdateRequest,
    KnowledgeResponse,
)

router = APIRouter(prefix="/knowledges", tags=["Knowledge"])


def get_knowledge_service(db: Session = Depends(get_db)) -> KnowledgeService:
    """Dependency untuk mendapatkan instance KnowledgeService."""
    return KnowledgeService(db)


@router.get("/", response_model=list[KnowledgeResponse])
def list_knowledges(
    ai_employee_id: UUID = Query(..., description="UUID AI employee pemilik knowledge"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    service: KnowledgeService = Depends(get_knowledge_service),
):
    """Mengambil daftar knowledge milik satu AI employee."""
    return service.list_knowledges(ai_employee_id)


@router.get("/{knowledge_id}", response_model=KnowledgeResponse)
def get_knowledge(
    knowledge_id: UUID,
    service: KnowledgeService = Depends(get_knowledge_service),
):
    """
    Mendapatkan satu knowledge berdasarkan ID.
    404 jika tidak ditemukan.
    """
    try:
        return service.get_knowledge(knowledge_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/", response_model=KnowledgeResponse, status_code=status.HTTP_201_CREATED)
def create_knowledge(
    request: KnowledgeCreateRequest,
    service: KnowledgeService = Depends(get_knowledge_service),
):
    """
    Menyimpan knowledge baru.
    404 jika AI employee tidak ditemukan,
    409 jika judul sudah ada pada AI yang sama,
    400 untuk validasi yang gagal.
    """
    try:
        return service.create_knowledge(request)
    except ValueError as e:
        msg = str(e).lower()
        if "ai employee not found" in msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        if "already exists" in msg:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{knowledge_id}", response_model=KnowledgeResponse)
def update_knowledge(
    knowledge_id: UUID,
    request: KnowledgeUpdateRequest,
    service: KnowledgeService = Depends(get_knowledge_service),
):
    """
    Memperbarui knowledge.
    404 jika tidak ditemukan,
    409 jika judul baru bentrok,
    400 untuk validasi.
    """
    try:
        return service.update_knowledge(knowledge_id, request)
    except ValueError as e:
        msg = str(e).lower()
        if "not found" in msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        if "already exists" in msg:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{knowledge_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_knowledge(
    knowledge_id: UUID,
    service: KnowledgeService = Depends(get_knowledge_service),
):
    """
    Menghapus knowledge.
    404 jika tidak ditemukan.
    """
    try:
        service.delete_knowledge(knowledge_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))