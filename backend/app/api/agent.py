"""
Agent API router — CRUD endpoints untuk AI Employee (disebut Agent di level API).
Prefix: /agents
Tag: Agents
"""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.repositories.ai_employee_repository import AIEmployeeRepository
from app.repositories.organization_repository import OrganizationRepository
from app.services.ai_employee_service import AIEmployeeService
from app.schemas.ai_employee import (
    AIEmployeeCreateRequest,
    AIEmployeeUpdateRequest,
    AIEmployeeResponse,
)

router = APIRouter(prefix="/agents", tags=["Agents"])


def get_ai_employee_service(db: Session = Depends(get_db)) -> AIEmployeeService:
    """Dependency untuk mendapatkan instance AIEmployeeService."""
    ai_employee_repo = AIEmployeeRepository(db)
    org_repo = OrganizationRepository(db)
    return AIEmployeeService(ai_employee_repo, org_repo)


@router.get("/", response_model=list[AIEmployeeResponse])
def list_agents(
    organization_id: UUID = Query(..., description="UUID organisasi"),
    skip: int = Query(0, ge=0, description="Jumlah data yang dilewati"),
    limit: int = Query(100, ge=1, le=500, description="Maksimum data yang dikembalikan"),
    service: AIEmployeeService = Depends(get_ai_employee_service),
):
    """Mengambil daftar AI agents dalam satu organisasi."""
    return service.list_ai_employees(organization_id)


@router.get("/{agent_id}", response_model=AIEmployeeResponse)
def get_agent(
    agent_id: UUID,
    service: AIEmployeeService = Depends(get_ai_employee_service),
):
    """
    Mendapatkan data satu agent berdasarkan ID.
    404 jika tidak ditemukan.
    """
    try:
        return service.get_ai_employee(agent_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/", response_model=AIEmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_agent(
    request: AIEmployeeCreateRequest,
    service: AIEmployeeService = Depends(get_ai_employee_service),
):
    """
    Membuat agent (AI employee) baru.
    404 jika organisasi tidak ditemukan,
    409 jika nama sudah ada di organisasi yang sama,
    400 jika provider tidak valid.
    """
    try:
        return service.create_ai_employee(request)
    except ValueError as e:
        msg = str(e).lower()
        if "organization not found" in msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        if "already exists" in msg:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
        if "unsupported provider" in msg:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{agent_id}", response_model=AIEmployeeResponse)
def update_agent(
    agent_id: UUID,
    request: AIEmployeeUpdateRequest,
    service: AIEmployeeService = Depends(get_ai_employee_service),
):
    """
    Memperbarui data agent.
    404 jika tidak ditemukan,
    409 jika nama baru bentrok,
    400 untuk error validasi lainnya.
    """
    try:
        return service.update_ai_employee(agent_id, request)
    except ValueError as e:
        msg = str(e).lower()
        if "not found" in msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        if "already exists" in msg:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_agent(
    agent_id: UUID,
    service: AIEmployeeService = Depends(get_ai_employee_service),
):
    """
    Menghapus agent.
    404 jika tidak ditemukan.
    """
    try:
        service.delete_ai_employee(agent_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))