"""
Workflow API router — CRUD endpoints untuk definisi workflow.
Prefix: /workflows
Tag: Workflows
"""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.repositories.workflow_repository import WorkflowRepository
from app.repositories.ai_employee_repository import AIEmployeeRepository
from app.services.workflow_service import WorkflowService
from app.schemas.workflow import (
    WorkflowCreateRequest,
    WorkflowUpdateRequest,
    WorkflowResponse,
)

router = APIRouter(prefix="/workflows", tags=["Workflows"])


def get_workflow_service(db: Session = Depends(get_db)) -> WorkflowService:
    """Dependency untuk mendapatkan instance WorkflowService."""
    workflow_repo = WorkflowRepository(db)
    ai_employee_repo = AIEmployeeRepository(db)
    return WorkflowService(workflow_repo, ai_employee_repo)


@router.get("/", response_model=list[WorkflowResponse])
def list_workflows(
    ai_employee_id: UUID = Query(..., description="UUID AI employee pemilik workflow"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    service: WorkflowService = Depends(get_workflow_service),
):
    """Mengambil daftar workflow milik satu AI employee."""
    return service.list_workflows(ai_employee_id)


@router.get("/{workflow_id}", response_model=WorkflowResponse)
def get_workflow(
    workflow_id: UUID,
    service: WorkflowService = Depends(get_workflow_service),
):
    """
    Mendapatkan satu workflow berdasarkan ID.
    404 jika tidak ditemukan.
    """
    try:
        return service.get_workflow(workflow_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/", response_model=WorkflowResponse, status_code=status.HTTP_201_CREATED)
def create_workflow(
    request: WorkflowCreateRequest,
    service: WorkflowService = Depends(get_workflow_service),
):
    """
    Membuat workflow baru.
    404 jika AI employee tidak ditemukan,
    409 jika nama sudah ada pada AI yang sama,
    400 untuk validasi yang gagal.
    """
    try:
        return service.create_workflow(request)
    except ValueError as e:
        msg = str(e).lower()
        if "ai employee not found" in msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        if "already exists" in msg:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{workflow_id}", response_model=WorkflowResponse)
def update_workflow(
    workflow_id: UUID,
    request: WorkflowUpdateRequest,
    service: WorkflowService = Depends(get_workflow_service),
):
    """
    Memperbarui workflow.
    404 jika tidak ditemukan,
    409 jika nama baru bentrok,
    400 untuk validasi.
    """
    try:
        return service.update_workflow(workflow_id, request)
    except ValueError as e:
        msg = str(e).lower()
        if "not found" in msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        if "already exists" in msg:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{workflow_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workflow(
    workflow_id: UUID,
    service: WorkflowService = Depends(get_workflow_service),
):
    """
    Menghapus workflow.
    404 jika tidak ditemukan.
    """
    try:
        service.delete_workflow(workflow_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))