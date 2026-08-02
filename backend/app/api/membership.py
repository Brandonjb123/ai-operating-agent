"""
Membership API router — CRUD endpoints untuk keanggotaan organisasi.
Menggunakan MembershipService, tanpa business logic.
"""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.repositories.membership_repository import MembershipRepository
from app.services.membership_service import MembershipService
from app.schemas.membership import (
    MembershipCreateRequest,
    MembershipUpdateRequest,
    MembershipResponse,
)

router = APIRouter(prefix="/memberships", tags=["Memberships"])


def get_membership_service(db: Session = Depends(get_db)) -> MembershipService:
    """Dependency untuk mendapatkan instance MembershipService."""
    repository = MembershipRepository(db)
    return MembershipService(repository)


@router.get("/", response_model=list[MembershipResponse])
def list_memberships(
    organization_id: UUID | None = Query(None, description="Filter by organization"),
    user_id: UUID | None = Query(None, description="Filter by user"),
    service: MembershipService = Depends(get_membership_service),
):
    """
    Mendaftar membership berdasarkan filter.
    Harus menyertakan salah satu: organization_id atau user_id, tidak keduanya.
    """
    if organization_id and user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provide only one of organization_id or user_id",
        )
    if organization_id:
        return service.list_by_organization(organization_id)
    if user_id:
        return service.list_by_user(user_id)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Provide either organization_id or user_id",
    )


@router.get("/{membership_id}", response_model=MembershipResponse)
def get_membership(
    membership_id: UUID,
    service: MembershipService = Depends(get_membership_service),
):
    """
    Mendapatkan data membership berdasarkan ID.
    404 jika tidak ditemukan.
    """
    try:
        return service.get_membership(membership_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post(
    "/", response_model=MembershipResponse, status_code=status.HTTP_201_CREATED
)
def create_membership(
    request: MembershipCreateRequest,
    service: MembershipService = Depends(get_membership_service),
):
    """
    Menambahkan pengguna ke organisasi dengan role tertentu.
    409 Conflict jika pengguna sudah menjadi anggota organisasi tersebut.
    """
    try:
        return service.create_membership(request)
    except ValueError as e:
        msg = str(e).lower()
        if "already belongs" in msg:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{membership_id}", response_model=MembershipResponse)
def update_membership(
    membership_id: UUID,
    request: MembershipUpdateRequest,
    service: MembershipService = Depends(get_membership_service),
):
    """
    Memperbarui role keanggotaan.
    404 jika membership tidak ditemukan.
    """
    try:
        return service.update_membership(membership_id, request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{membership_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_membership(
    membership_id: UUID,
    service: MembershipService = Depends(get_membership_service),
):
    """
    Menghapus keanggotaan (mengeluarkan pengguna dari organisasi).
    404 jika tidak ditemukan.
    """
    try:
        service.delete_membership(membership_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))