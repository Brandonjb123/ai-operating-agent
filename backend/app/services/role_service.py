"""
Role Service — logika bisnis untuk manajemen role.
Menggunakan RoleRepository, tanpa akses database langsung.
"""

from uuid import UUID
from app.models.role import Role
from app.repositories.role_repository import RoleRepository
from app.schemas.role import RoleCreateRequest, RoleUpdateRequest, RoleResponse


class RoleService:
    """Service layer untuk operasi role dalam suatu organisasi."""

    def __init__(self, repository: RoleRepository) -> None:
        """
        Inisialisasi dengan repository yang di-inject.

        Args:
            repository (RoleRepository): Instance RoleRepository.
        """
        self.repository = repository

    def list_roles(self, organization_id: UUID) -> list[RoleResponse]:
        """
        Mengambil semua role untuk organisasi tertentu.

        Args:
            organization_id (UUID): UUID organisasi.

        Returns:
            list[RoleResponse]: Daftar role.
        """
        roles = self.repository.list(organization_id)
        return [RoleResponse.model_validate(r) for r in roles]

    def get_role(self, role_id: UUID) -> RoleResponse:
        """
        Mendapatkan role berdasarkan ID.

        Args:
            role_id (UUID): UUID role.

        Returns:
            RoleResponse: Data role.

        Raises:
            ValueError: Jika role tidak ditemukan.
        """
        role = self.repository.get_by_id(role_id)
        if role is None:
            raise ValueError("Role not found")
        return RoleResponse.model_validate(role)

    def create_role(self, request: RoleCreateRequest) -> RoleResponse:
        """
        Membuat role baru dengan validasi duplikasi nama dalam organisasi yang sama.

        Args:
            request (RoleCreateRequest): Data pembuatan role.

        Returns:
            RoleResponse: Role yang baru dibuat.

        Raises:
            ValueError: Jika nama sudah ada di organisasi tersebut.
        """
        name = request.name.strip()
        if not name:
            raise ValueError("Role name cannot be empty")

        # Cek duplikasi (case-insensitive) hanya dalam satu organisasi
        existing = self.repository.get_by_name(
            organization_id=request.organization_id,
            name=name.lower()  # simpan lowercase untuk pengecekan
        )
        if existing:
            raise ValueError("Role already exists")

        # Simpan nama asli (capitalization dipertahankan)
        role = Role(
            organization_id=request.organization_id,
            name=request.name.strip(),          # original casing
            description=request.description,
        )
        saved = self.repository.create(role)
        return RoleResponse.model_validate(saved)

    def update_role(
        self, role_id: UUID, request: RoleUpdateRequest
    ) -> RoleResponse:
        """
        Memperbarui data role. Hanya field yang tidak None yang diupdate.

        Args:
            role_id (UUID): ID role yang akan diupdate.
            request (RoleUpdateRequest): Data baru (parsial).

        Returns:
            RoleResponse: Role setelah update.

        Raises:
            ValueError: Jika role tidak ditemukan atau nama baru sudah ada.
        """
        role = self.repository.get_by_id(role_id)
        if role is None:
            raise ValueError("Role not found")

        # Jika nama diubah, validasi duplikasi (case-insensitive)
        if request.name is not None:
            new_name = request.name.strip()
            if not new_name:
                raise ValueError("Role name cannot be empty")
            # Cek apakah sudah ada nama yang sama (case-insensitive) selain dirinya sendiri
            existing = self.repository.get_by_name(
                organization_id=role.organization_id,
                name=new_name.lower()
            )
            if existing and existing.id != role_id:
                raise ValueError("Role already exists")
            role.name = request.name.strip()  # simpan dengan casing asli

        if request.description is not None:
            role.description = request.description

        updated = self.repository.update(role)
        return RoleResponse.model_validate(updated)
    

    def delete_role(self, role_id: UUID) -> None:
        """
        Menghapus role berdasarkan ID.

        Args:
            role_id (UUID): ID role yang akan dihapus.

        Raises:
            ValueError: Jika role tidak ditemukan.
        """
        role = self.repository.get_by_id(role_id)
        if role is None:
            raise ValueError("Role not found")
        self.repository.delete(role)