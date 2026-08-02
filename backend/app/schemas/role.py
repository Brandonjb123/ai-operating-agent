from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

class RoleCreateRequest(BaseModel):
    organization_id: UUID
    name: str = Field(..., min_length=1)
    description: str | None = None
    # status dihapus karena model tidak punya

class RoleUpdateRequest(BaseModel):
    name: str | None = Field(None, min_length=1)
    description: str | None = None

class RoleResponse(BaseModel):
    id: UUID
    organization_id: UUID
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}