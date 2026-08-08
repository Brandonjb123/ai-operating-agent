"""
Schema untuk Knowledge: request & response.
Menggunakan Pydantic v2 dengan validasi field.
"""

from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, field_validator

ALLOWED_KNOWLEDGE_TYPES = {"document", "faq", "manual", "policy", "note"}
ALLOWED_STATUSES = {"active", "inactive", "archived"}


class KnowledgeCreateRequest(BaseModel):
    """Body request untuk membuat knowledge baru."""
    ai_employee_id: UUID = Field(..., description="UUID AI employee pemilik")
    title: str = Field(..., min_length=1, description="Judul knowledge")
    content: str = Field(..., min_length=1, description="Isi knowledge")
    source: str = Field(..., min_length=1, description="Sumber knowledge (manual, upload, api, dll)")
    knowledge_type: str = Field(default="document", description="Tipe knowledge (document, faq, dll)")
    status: str = Field(default="active", description="Status knowledge (active, inactive, archived)")
    metadata_: dict | None = Field(None, alias="metadata", description="Metadata tambahan (JSON)")

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Knowledge title is required")
        return v.strip()

    @field_validator("content")
    @classmethod
    def content_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Content is required")
        return v

    @field_validator("source")
    @classmethod
    def source_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Source is required")
        return v.strip()

    @field_validator("knowledge_type")
    @classmethod
    def validate_knowledge_type(cls, v: str) -> str:
        if v.lower() not in ALLOWED_KNOWLEDGE_TYPES:
            raise ValueError(f"Unsupported knowledge type '{v}'. Allowed: {', '.join(sorted(ALLOWED_KNOWLEDGE_TYPES))}")
        return v.lower()

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        if v.lower() not in ALLOWED_STATUSES:
            raise ValueError(f"Invalid status '{v}'. Allowed: {', '.join(sorted(ALLOWED_STATUSES))}")
        return v.lower()

    class Config:
        populate_by_name = True


class KnowledgeUpdateRequest(BaseModel):
    """Body request untuk mengupdate knowledge. Semua field opsional."""
    title: str | None = Field(None, min_length=1)
    content: str | None = Field(None, min_length=1)
    source: str | None = None
    knowledge_type: str | None = None
    status: str | None = None
    metadata_: dict | None = Field(None, alias="metadata")

    @field_validator("knowledge_type")
    @classmethod
    def validate_knowledge_type(cls, v: str | None) -> str | None:
        if v is not None and v.lower() not in ALLOWED_KNOWLEDGE_TYPES:
            raise ValueError(f"Unsupported knowledge type '{v}'")
        return v.lower() if v else v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str | None) -> str | None:
        if v is not None and v.lower() not in ALLOWED_STATUSES:
            raise ValueError(f"Invalid status '{v}'")
        return v.lower() if v else v

    class Config:
        populate_by_name = True


class KnowledgeResponse(BaseModel):
    """Skema respons untuk menampilkan data knowledge."""
    id: UUID
    organization_id: UUID
    ai_employee_id: UUID
    title: str
    content: str
    source: str
    knowledge_type: str
    status: str
    metadata_: dict | None = Field(
        default=None,
        validation_alias="metadata_",   # membaca dari objek SQLAlchemy (metadata_)
        serialization_alias="metadata"  # tampil sebagai "metadata" di JSON
    )
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }