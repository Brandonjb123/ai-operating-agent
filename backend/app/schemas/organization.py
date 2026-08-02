"""
Skema untuk Organization: request & response.
Menggunakan Pydantic v2.
"""

from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field


class OrganizationCreateRequest(BaseModel):
    """Body request untuk membuat organisasi baru."""
    name: str = Field(..., min_length=1, description="Nama organisasi")
    slug: str = Field(..., min_length=1, description="Slug unik, lowercase")
    description: str | None = None
    logo_url: str | None = None
    website: str | None = None
    status: str = "active"


class OrganizationUpdateRequest(BaseModel):
    """Body request untuk memperbarui organisasi. Semua field opsional."""
    name: str | None = Field(None, min_length=1)
    slug: str | None = Field(None, min_length=1)
    description: str | None = None
    logo_url: str | None = None
    website: str | None = None
    status: str | None = None


class OrganizationResponse(BaseModel):
    """Skema respons untuk menampilkan data organisasi."""
    id: UUID
    name: str
    slug: str
    description: str | None
    logo_url: str | None
    website: str | None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}