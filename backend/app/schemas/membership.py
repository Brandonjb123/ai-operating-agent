"""
Skema untuk Membership: request & response.
Menggunakan Pydantic v2.
"""

from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field


class MembershipCreateRequest(BaseModel):
    """Body request untuk menambahkan user ke organisasi dengan role tertentu."""
    organization_id: UUID = Field(..., description="UUID organisasi")
    user_id: UUID = Field(..., description="UUID pengguna yang akan ditambahkan")
    role_id: UUID = Field(..., description="UUID role untuk pengguna")


class MembershipUpdateRequest(BaseModel):
    """Body request untuk memperbarui membership (hanya role yang bisa diganti)."""
    role_id: UUID | None = Field(None, description="UUID role baru")


class MembershipResponse(BaseModel):
    """Skema respons untuk menampilkan data membership."""
    id: UUID
    organization_id: UUID
    user_id: UUID
    role_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}