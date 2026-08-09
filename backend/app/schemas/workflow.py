"""
Schema untuk Workflow: request & response.
Menggunakan Pydantic v2 dengan validasi field.
"""

from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, field_validator

ALLOWED_TRIGGER_TYPES = {"manual", "api", "schedule", "event"}
ALLOWED_STATUSES = {"active", "inactive"}


class WorkflowCreateRequest(BaseModel):
    """Body request untuk membuat workflow baru."""
    ai_employee_id: UUID = Field(..., description="UUID AI employee pemilik")
    name: str = Field(..., min_length=1, description="Nama workflow")
    description: str | None = None
    definition: dict = Field(..., description="Definisi workflow dalam format JSON")
    trigger_type: str = Field(default="manual", description="Tipe pemicu workflow")
    status: str = Field(default="active", description="Status workflow")

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Workflow name is required")
        return v.strip()

    @field_validator("trigger_type")
    @classmethod
    def validate_trigger_type(cls, v: str) -> str:
        if v.lower() not in ALLOWED_TRIGGER_TYPES:
            raise ValueError(f"Unsupported trigger type '{v}'. Allowed: {', '.join(sorted(ALLOWED_TRIGGER_TYPES))}")
        return v.lower()

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        if v.lower() not in ALLOWED_STATUSES:
            raise ValueError(f"Invalid status '{v}'. Allowed: {', '.join(sorted(ALLOWED_STATUSES))}")
        return v.lower()


class WorkflowUpdateRequest(BaseModel):
    """Body request untuk memperbarui workflow. Semua field opsional."""
    name: str | None = Field(None, min_length=1)
    description: str | None = None
    definition: dict | None = None
    trigger_type: str | None = None
    status: str | None = None

    @field_validator("trigger_type")
    @classmethod
    def validate_trigger_type(cls, v: str | None) -> str | None:
        if v is not None and v.lower() not in ALLOWED_TRIGGER_TYPES:
            raise ValueError(f"Unsupported trigger type '{v}'")
        return v.lower() if v else v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str | None) -> str | None:
        if v is not None and v.lower() not in ALLOWED_STATUSES:
            raise ValueError(f"Invalid status '{v}'")
        return v.lower() if v else v


class WorkflowResponse(BaseModel):
    """Skema respons untuk menampilkan data workflow."""
    id: UUID
    organization_id: UUID
    ai_employee_id: UUID
    name: str
    description: str | None
    definition: dict
    trigger_type: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}