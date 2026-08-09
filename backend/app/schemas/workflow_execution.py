"""
Schema untuk WorkflowExecution: request & response.
Menggunakan Pydantic v2 dengan validasi field.
"""

from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, field_validator

ALLOWED_EXECUTION_STATUSES = {"pending", "running", "completed", "failed", "cancelled"}
ALLOWED_TRIGGER_TYPES = {"manual", "api", "schedule", "event"}


class WorkflowExecutionCreateRequest(BaseModel):
    """Request untuk membuat execution baru."""
    workflow_id: UUID = Field(..., description="UUID workflow yang akan dieksekusi")
    ai_employee_id: UUID = Field(..., description="UUID AI employee yang menjalankan")
    trigger_type: str = Field(default="manual", description="Pemicu eksekusi")
    input_data: dict | None = Field(default=None, description="Data input awal (JSON)")

    @field_validator("trigger_type")
    @classmethod
    def validate_trigger_type(cls, v: str) -> str:
        if v.lower() not in ALLOWED_TRIGGER_TYPES:
            raise ValueError(f"Unsupported trigger type '{v}'. Allowed: {', '.join(sorted(ALLOWED_TRIGGER_TYPES))}")
        return v.lower()


class WorkflowExecutionUpdateRequest(BaseModel):
    """Request untuk update execution. Hanya field yang diberikan yang diubah."""
    status: str | None = Field(None, description="Status execution (pending, running, completed, failed, cancelled)")
    input_data: dict | None = Field(None, description="Update input data")
    output_data: dict | None = Field(None, description="Update output data")
    error_message: str | None = Field(None, description="Pesan error jika gagal")
    started_at: datetime | None = Field(None, description="Waktu mulai eksekusi")
    completed_at: datetime | None = Field(None, description="Waktu selesai eksekusi")

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str | None) -> str | None:
        if v is not None and v.lower() not in ALLOWED_EXECUTION_STATUSES:
            raise ValueError(f"Invalid status '{v}'. Allowed: {', '.join(sorted(ALLOWED_EXECUTION_STATUSES))}")
        return v.lower() if v else v


class WorkflowExecutionResponse(BaseModel):
    """Response untuk menampilkan data execution."""
    id: UUID
    organization_id: UUID
    workflow_id: UUID
    ai_employee_id: UUID
    status: str
    trigger_type: str
    input_data: dict | None
    output_data: dict | None
    error_message: str | None
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class RunExecutionRequest(BaseModel):
    execution_id: UUID = Field(..., description="UUID execution yang akan dijalankan")    