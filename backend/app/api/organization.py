"""
Organization API router — CRUD endpoints untuk organisasi.
Menggunakan OrganizationService, tanpa business logic.
"""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.repositories.organization_repository import OrganizationRepository
from app.services.organization_service import OrganizationService
from app.schemas.organization import (
    OrganizationCreateRequest,
    OrganizationUpdateRequest,
    OrganizationResponse,
)

router = APIRouter(prefix="/organizations", tags=["Organizations"])


# Dependency helper untuk mendapatkan service (menghindari duplikasi)
def get_organization_service(db: Session = Depends(get_db)) -> OrganizationService:
    """Inisialisasi OrganizationService dengan session & repository."""
    repository = OrganizationRepository(db)
    return OrganizationService(repository)


@router.get("/", response_model=list[OrganizationResponse])
def list_organizations(
    service: OrganizationService = Depends(get_organization_service),
):
    """Mengambil daftar semua organisasi."""
    return service.list_organizations()


@router.get("/{organization_id}", response_model=OrganizationResponse)
def get_organization(
    organization_id: UUID,
    service: OrganizationService = Depends(get_organization_service),
):
    """
    Mendapatkan data organisasi berdasarkan ID.
    Mengembalikan 404 jika tidak ditemukan.
    """
    try:
        return service.get_organization(organization_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
def create_organization(
    request: OrganizationCreateRequest,
    service: OrganizationService = Depends(get_organization_service),
):
    """
    Membuat organisasi baru.
    Mengembalikan 409 Conflict jika slug sudah ada.
    """
    try:
        return service.create_organization(request)
    except ValueError as e:
        msg = str(e).lower()
        if "already exists" in msg or "slug" in msg:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{organization_id}", response_model=OrganizationResponse)
def update_organization(
    organization_id: UUID,
    request: OrganizationUpdateRequest,
    service: OrganizationService = Depends(get_organization_service),
):
    """
    Memperbarui data organisasi.
    Mengembalikan 404 jika tidak ditemukan, 409 jika slug bentrok.
    """
    try:
        return service.update_organization(organization_id, request)
    except ValueError as e:
        msg = str(e).lower()
        if "not found" in msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        if "already exists" in msg or "slug" in msg:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{organization_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_organization(
    organization_id: UUID,
    service: OrganizationService = Depends(get_organization_service),
):
    """
    Menghapus organisasi.
    Mengembalikan 404 jika tidak ditemukan.
    """
    try:
        service.delete_organization(organization_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))