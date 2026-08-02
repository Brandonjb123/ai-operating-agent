"""
Organization Service — berisi semua logika bisnis terkait organisasi.
Tidak menyentuh database secara langsung; menggunakan OrganizationRepository.
"""

from uuid import UUID
from app.models.organization import Organization
from app.repositories.organization_repository import OrganizationRepository
from app.schemas.organization import (
    OrganizationCreateRequest,
    OrganizationUpdateRequest,
    OrganizationResponse,
)


class OrganizationService:
    """
    Service layer untuk manajemen organisasi.
    """

    def __init__(self, repository: OrganizationRepository) -> None:
        """
        Inisialisasi service dengan repository yang di-inject.

        Args:
            repository (OrganizationRepository): Instance OrganizationRepository.
        """
        self.repository = repository

    def list_organizations(self) -> list[OrganizationResponse]:
        """
        Mengambil daftar semua organisasi.

        Returns:
            list[OrganizationResponse]: Daftar organisasi.
        """
        orgs = self.repository.list()
        return [OrganizationResponse.model_validate(org) for org in orgs]

    def get_organization(self, organization_id: UUID) -> OrganizationResponse:
        """
        Mendapatkan organisasi berdasarkan ID.

        Args:
            organization_id (UUID): UUID organisasi.

        Returns:
            OrganizationResponse: Data organisasi.

        Raises:
            ValueError: Jika organisasi tidak ditemukan.
        """
        org = self.repository.get_by_id(organization_id)
        if org is None:
            raise ValueError("Organization not found")
        return OrganizationResponse.model_validate(org)

    def create_organization(
        self, request: OrganizationCreateRequest
    ) -> OrganizationResponse:
        """
        Membuat organisasi baru dengan aturan bisnis.

        Args:
            request (OrganizationCreateRequest): Data pembuatan organisasi.

        Returns:
            OrganizationResponse: Data organisasi yang baru dibuat.

        Raises:
            ValueError: Jika slug sudah ada atau nama/slug kosong.
        """
        # Normalisasi
        name = request.name.strip()
        slug = request.slug.strip().lower()

        if not name:
            raise ValueError("Organization name cannot be empty")
        if not slug:
            raise ValueError("Organization slug cannot be empty")

        # Cek slug unik
        existing = self.repository.get_by_slug(slug)
        if existing:
            raise ValueError("Organization slug already exists")

        # Buat entitas
        org = Organization(
            name=name,
            slug=slug,
            description=request.description,
            logo_url=request.logo_url,
            website=request.website,
            status=request.status or "active",
        )

        saved = self.repository.create(org)
        return OrganizationResponse.model_validate(saved)

    def update_organization(
        self, organization_id: UUID, request: OrganizationUpdateRequest
    ) -> OrganizationResponse:
        """
        Memperbarui data organisasi. Hanya field yang tidak None yang diupdate.

        Args:
            organization_id (UUID): ID organisasi yang akan diupdate.
            request (OrganizationUpdateRequest): Data baru (parsial).

        Returns:
            OrganizationResponse: Data organisasi setelah update.

        Raises:
            ValueError: Jika organisasi tidak ditemukan atau slug baru sudah ada.
        """
        org = self.repository.get_by_id(organization_id)
        if org is None:
            raise ValueError("Organization not found")

        # Normalisasi slug jika diubah
        if request.slug is not None:
            new_slug = request.slug.strip().lower()
            if not new_slug:
                raise ValueError("Slug cannot be empty")
            # Cek duplikasi slug (kecuali slug milik sendiri)
            existing = self.repository.get_by_slug(new_slug)
            if existing and existing.id != organization_id:
                raise ValueError("Organization slug already exists")
            org.slug = new_slug

        # Update field yang disediakan (None = tidak diubah)
        if request.name is not None:
            org.name = request.name.strip()
            if not org.name:
                raise ValueError("Name cannot be empty")
        if request.description is not None:
            org.description = request.description
        if request.logo_url is not None:
            org.logo_url = request.logo_url
        if request.website is not None:
            org.website = request.website
        if request.status is not None:
            org.status = request.status

        updated = self.repository.update(org)
        return OrganizationResponse.model_validate(updated)

    def delete_organization(self, organization_id: UUID) -> None:
        """
        Menghapus organisasi berdasarkan ID.

        Args:
            organization_id (UUID): ID organisasi yang akan dihapus.

        Raises:
            ValueError: Jika organisasi tidak ditemukan.
        """
        org = self.repository.get_by_id(organization_id)
        if org is None:
            raise ValueError("Organization not found")
        self.repository.delete(org)