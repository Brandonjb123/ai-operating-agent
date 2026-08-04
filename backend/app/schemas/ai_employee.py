"""
Skema untuk AIEmployee: request & response.
Menggunakan Pydantic v2, validasi ketat.
"""

from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, field_validator

ALLOWED_PROVIDERS = {"groq", "openai", "anthropic", "google", "ollama"}


class AIEmployeeCreateRequest(BaseModel):
    """Body request untuk membuat AI employee baru."""
    organization_id: UUID = Field(..., description="UUID organisasi pemilik")
    name: str = Field(..., min_length=1, description="Nama AI employee")
    description: str | None = None
    avatar_url: str | None = None
    provider: str = Field(default="groq", description="Provider LLM (groq, openai, dll)")
    model: str = Field(default="llama3-8b-8192", description="Nama model LLM")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Suhu kreativitas (0-2)")
    max_tokens: int = Field(default=4096, gt=0, description="Maksimum token output")
    system_prompt: str = Field(
        default="You are a helpful AI assistant.",
        min_length=1,
        description="Prompt sistem awal"
    )
    status: str = Field(default="active", description="Status (active/inactive)")

    @field_validator("provider")
    @classmethod
    def validate_provider(cls, v: str) -> str:
        if v.lower() not in ALLOWED_PROVIDERS:
            raise ValueError(f"Unsupported provider '{v}'. Allowed: {', '.join(sorted(ALLOWED_PROVIDERS))}")
        return v.lower()

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("AI employee name is required")
        return v.strip()

    @field_validator("system_prompt")
    @classmethod
    def prompt_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("System prompt cannot be empty")
        return v


class AIEmployeeUpdateRequest(BaseModel):
    """Body request untuk update AI employee. Semua field opsional."""
    name: str | None = Field(None, min_length=1)
    description: str | None = None
    avatar_url: str | None = None
    provider: str | None = None
    model: str | None = None
    temperature: float | None = Field(None, ge=0.0, le=2.0)
    max_tokens: int | None = Field(None, gt=0)
    system_prompt: str | None = Field(None, min_length=1)
    status: str | None = None

    @field_validator("provider")
    @classmethod
    def validate_provider(cls, v: str | None) -> str | None:
        if v is not None and v.lower() not in ALLOWED_PROVIDERS:
            raise ValueError(f"Unsupported provider '{v}'. Allowed: {', '.join(sorted(ALLOWED_PROVIDERS))}")
        return v.lower() if v else v


class AIEmployeeResponse(BaseModel):
    """Skema respons untuk menampilkan data AI employee."""
    id: UUID
    organization_id: UUID
    name: str
    description: str | None
    avatar_url: str | None
    provider: str
    model: str
    temperature: float
    max_tokens: int
    system_prompt: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}