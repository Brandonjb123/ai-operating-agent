"""
Membership Repository — akses data untuk entitas Membership.
Menggunakan SQLAlchemy 2.0 style, Session injection, tanpa business logic.
"""

from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.membership import Membership


class MembershipRepository:
    """
    Repository untuk entitas Membership.
    Menyediakan operasi dasar CRUD dan pencarian berdasarkan organisasi/user.
    """

    def __init__(self, db: Session) -> None:
        """
        Inisialisasi repository dengan session database yang di-inject.

        Args:
            db (Session): SQLAlchemy Session aktif.
        """
        self.db = db

    def get_by_id(self, membership_id: UUID) -> Membership | None:
        """
        Mencari membership berdasarkan ID.

        Args:
            membership_id (UUID): UUID membership.

        Returns:
            Membership | None: Objek membership jika ditemukan, None jika tidak.
        """
        stmt = select(Membership).where(Membership.id == membership_id)
        return self.db.scalar(stmt)

    def get_membership(
        self, organization_id: UUID, user_id: UUID
    ) -> Membership | None:
        """
        Mencari membership berdasarkan kombinasi organisasi dan user.

        Args:
            organization_id (UUID): UUID organisasi.
            user_id (UUID): UUID user.

        Returns:
            Membership | None: Membership jika pengguna adalah anggota organisasi.
        """
        stmt = (
            select(Membership)
            .where(Membership.organization_id == organization_id)
            .where(Membership.user_id == user_id)
        )
        return self.db.scalar(stmt)

    def list_by_organization(
        self, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[Membership]:
        """
        Mengambil daftar membership untuk satu organisasi (dengan paginasi).

        Args:
            organization_id (UUID): UUID organisasi.
            skip (int): Offset data.
            limit (int): Maksimum data.

        Returns:
            list[Membership]: Daftar membership dalam organisasi tersebut.
        """
        stmt = (
            select(Membership)
            .where(Membership.organization_id == organization_id)
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())

    def list_by_user(self, user_id: UUID) -> list[Membership]:
        """
        Mengambil semua membership yang dimiliki seorang user.

        Args:
            user_id (UUID): UUID user.

        Returns:
            list[Membership]: Daftar membership pengguna.
        """
        stmt = select(Membership).where(Membership.user_id == user_id)
        return list(self.db.scalars(stmt).all())

    def create(self, membership: Membership) -> Membership:
        """
        Menyimpan membership baru ke database.

        Args:
            membership (Membership): Objek membership yang akan disimpan.

        Returns:
            Membership: Objek membership yang sudah disimpan (termasuk ID).
        """
        self.db.add(membership)
        self.db.commit()
        self.db.refresh(membership)
        return membership

    def update(self, membership: Membership) -> Membership:
        """
        Memperbarui data membership.

        Args:
            membership (Membership): Objek membership dengan data terbaru.

        Returns:
            Membership: Membership yang sudah diperbarui.
        """
        self.db.merge(membership)
        self.db.commit()
        self.db.refresh(membership)
        return membership

    def delete(self, membership: Membership) -> None:
        """
        Menghapus membership dari database.

        Args:
            membership (Membership): Objek membership yang akan dihapus.
        """
        self.db.delete(membership)
        self.db.commit()