"""
Schema untuk Memory: request & response.
Menggunakan Pydantic v2 dengan validasi field.
"""

from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, field_validator

ALLOWED_MEMORY_TYPES = {"long_term", "short_term", "episodic", "semantic"}


class MemoryCreateRequest(BaseModel):
    """Body request untuk menyimpan memory baru."""
    ai_employee_id: UUID = Field(..., description="UUID AI employee pemilik memory")
    memory_key: str = Field(..., min_length=1, description="Kunci unik memory dalam satu AI employee")
    memory_value: str = Field(..., min_length=1, description="Isi memory")
    memory_type: str = Field(default="long_term", description="Tipe memory (long_term, short_term, dll)")
    importance: int = Field(default=1, ge=1, le=10, description="Tingkat kepentingan (1-10)")
    metadata_: dict | None = Field(None, alias="metadata", description="Metadata tambahan (JSON)")

    @field_validator("memory_key")
    @classmethod
    def key_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Memory key is required")
        return v.strip()

    @field_validator("memory_value")
    @classmethod
    def value_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Memory value is required")
        return v

    @field_validator("memory_type")
    @classmethod
    def validate_memory_type(cls, v: str) -> str:
        if v.lower() not in ALLOWED_MEMORY_TYPES:
            raise ValueError(f"Unsupported memory type '{v}'. Allowed: {', '.join(sorted(ALLOWED_MEMORY_TYPES))}")
        return v.lower()

    class Config:
        populate_by_name = True


class MemoryUpdateRequest(BaseModel):
    """Body request untuk mengupdate memory (semua field opsional)."""
    memory_key: str | None = Field(None, min_length=1)
    memory_value: str | None = Field(None, min_length=1)
    memory_type: str | None = None
    importance: int | None = Field(None, ge=1, le=10)
    metadata_: dict | None = Field(None, alias="metadata")

    @field_validator("memory_type")
    @classmethod
    def validate_memory_type(cls, v: str | None) -> str | None:
        if v is not None and v.lower() not in ALLOWED_MEMORY_TYPES:
            raise ValueError(f"Unsupported memory type '{v}'")
        return v.lower() if v else v

    class Config:
        populate_by_name = True


class MemoryResponse(BaseModel):
    """Skema respons untuk menampilkan data memory."""
    id: UUID
    organization_id: UUID
    ai_employee_id: UUID
    memory_key: str
    memory_value: str
    memory_type: str
    importance: int
    metadata_: dict | None = Field(
        default=None,
        validation_alias="metadata_",
        serialization_alias="metadata"
    )
    last_accessed_at: datetime | None
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }