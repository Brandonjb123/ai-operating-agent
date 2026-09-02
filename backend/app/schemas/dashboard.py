"""Response schemas for dashboard summary endpoints."""

from pydantic import BaseModel, Field


class DashboardSummaryResponse(BaseModel):
    """Organization-scoped counts displayed on the dashboard."""

    total_digital_employees: int = Field(ge=0)
    active_digital_employees: int = Field(ge=0)
    total_knowledge: int = Field(ge=0)
    total_memory: int = Field(ge=0)
    total_workflows: int = Field(ge=0)
