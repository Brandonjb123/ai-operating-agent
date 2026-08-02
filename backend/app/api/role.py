"""
Role API router — CRUD endpoints untuk manajemen role dalam organisasi.
Menggunakan RoleService, tanpa business logic.
"""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.repositories.role_repository import RoleRepository
from app.services.role_service import RoleService
from app.schemas.role import RoleCreateRequest, RoleUpdateRequest, RoleResponse

router = APIRouter(prefix="/roles", tags=["Roles"])


def get_role_service(db: Session = Depends(get_db)) -> RoleService:
    """Dependency untuk mendapatkan instance RoleService."""
    repository = RoleRepository(db)
    return RoleService(repository)


@router.get("/", response_model=list[RoleResponse])
def list_roles(
    organization_id: UUID = Query(..., description="UUID organisasi"),
    service: RoleService = Depends(get_role_service),
):
    """Mengambil daftar role untuk organisasi tertentu."""
    return service.list_roles(organization_id)


@router.get("/{role_id}", response_model=RoleResponse)
def get_role(
    role_id: UUID,
    service: RoleService = Depends(get_role_service),
):
    """
    Mendapatkan data role berdasarkan ID.
    Mengembalikan 404 jika tidak ditemukan.
    """
    try:
        return service.get_role(role_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(
    request: RoleCreateRequest,
    service: RoleService = Depends(get_role_service),
):
    """
    Membuat role baru.
    Mengembalikan 409 Conflict jika nama sudah ada di organisasi yang sama.
    """
    try:
        return service.create_role(request)
    except ValueError as e:
        msg = str(e).lower()
        if "already exists" in msg:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{role_id}", response_model=RoleResponse)
def update_role(
    role_id: UUID,
    request: RoleUpdateRequest,
    service: RoleService = Depends(get_role_service),
):
    """
    Memperbarui data role.
    Mengembalikan 404 jika tidak ditemukan, 409 jika nama bentrok.
    """
    try:
        return service.update_role(role_id, request)
    except ValueError as e:
        msg = str(e).lower()
        if "not found" in msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        if "already exists" in msg:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(
    role_id: UUID,
    service: RoleService = Depends(get_role_service),
):
    """
    Menghapus role.
    Mengembalikan 404 jika tidak ditemukan.
    """
    try:
        service.delete_role(role_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))