"""
Membership Service — logika bisnis keanggotaan organisasi.
Mencegah duplikasi keanggotaan, mengelola role, dll.
"""

from uuid import UUID
from app.models.membership import Membership
from app.repositories.membership_repository import MembershipRepository
from app.schemas.membership import (
    MembershipCreateRequest,
    MembershipUpdateRequest,
    MembershipResponse,
)
from datetime import datetime, timezone

class MembershipService:
    """Service untuk manajemen keanggotaan pengguna dalam organisasi."""

    def __init__(self, repository: MembershipRepository) -> None:
        """
        Inisialisasi dengan repository yang di-inject.

        Args:
            repository (MembershipRepository): Instance repository.
        """
        self.repository = repository

    def list_by_organization(
        self, organization_id: UUID
    ) -> list[MembershipResponse]:
        """
        Mendaftar seluruh anggota dari satu organisasi.

        Args:
            organization_id (UUID): UUID organisasi.

        Returns:
            list[MembershipResponse]: Daftar membership.
        """
        memberships = self.repository.list_by_organization(organization_id)
        return [MembershipResponse.model_validate(m) for m in memberships]

    def list_by_user(self, user_id: UUID) -> list[MembershipResponse]:
        """
        Mendaftar seluruh keanggotaan seorang user di berbagai organisasi.

        Args:
            user_id (UUID): UUID pengguna.

        Returns:
            list[MembershipResponse]: Daftar membership pengguna.
        """
        memberships = self.repository.list_by_user(user_id)
        return [MembershipResponse.model_validate(m) for m in memberships]

    def get_membership(self, membership_id: UUID) -> MembershipResponse:
        """
        Mendapatkan satu membership berdasarkan ID.

        Args:
            membership_id (UUID): UUID membership.

        Returns:
            MembershipResponse: Data membership.

        Raises:
            ValueError: Jika membership tidak ditemukan.
        """
        membership = self.repository.get_by_id(membership_id)
        if membership is None:
            raise ValueError("Membership not found")
        return MembershipResponse.model_validate(membership)

    def create_membership(
        self, request: MembershipCreateRequest
    ) -> MembershipResponse:
        """
        Menambahkan pengguna ke organisasi dengan role tertentu.

        Aturan bisnis:
        - Satu pengguna hanya boleh menjadi anggota satu organisasi sekali.
        - organization_id, user_id, role_id wajib.

        Args:
            request (MembershipCreateRequest): Data membership baru.

        Returns:
            MembershipResponse: Membership yang baru dibuat.

        Raises:
            ValueError: Jika pengguna sudah menjadi anggota organisasi.
        """
        # Cek apakah sudah ada membership untuk user dan organisasi yang sama
        existing = self.repository.get_membership(
            request.organization_id, request.user_id
        )
        if existing:
            raise ValueError("User already belongs to organization")

        # Buat entitas membership
        membership = Membership(
            organization_id=request.organization_id,
            user_id=request.user_id,
            role_id=request.role_id,
            joined_at=datetime.now(timezone.utc)
        )
        saved = self.repository.create(membership)
        return MembershipResponse.model_validate(saved)

    def update_membership(
        self, membership_id: UUID, request: MembershipUpdateRequest
    ) -> MembershipResponse:
        """
        Memperbarui role pengguna dalam organisasi.

        Args:
            membership_id (UUID): ID membership yang akan diupdate.
            request (MembershipUpdateRequest): Data role baru (jika tidak None).

        Returns:
            MembershipResponse: Membership setelah update.

        Raises:
            ValueError: Jika membership tidak ditemukan.
        """
        membership = self.repository.get_by_id(membership_id)
        if membership is None:
            raise ValueError("Membership not found")

        # Hanya role yang bisa diubah
        if request.role_id is not None:
            membership.role_id = request.role_id

        updated = self.repository.update(membership)
        return MembershipResponse.model_validate(updated)

    def delete_membership(self, membership_id: UUID) -> None:
        """
        Menghapus keanggotaan (mengeluarkan pengguna dari organisasi).

        Args:
            membership_id (UUID): ID membership yang akan dihapus.

        Raises:
            ValueError: Jika membership tidak ditemukan.
        """
        membership = self.repository.get_by_id(membership_id)
        if membership is None:
            raise ValueError("Membership not found")
        self.repository.delete(membership)