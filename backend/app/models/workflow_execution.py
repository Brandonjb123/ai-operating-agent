"""
WorkflowExecution Model — instance eksekusi dari Workflow Definition.
"""

import uuid
from datetime import datetime
from sqlalchemy import String, Text, ForeignKey, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base_model import BaseModel


class WorkflowExecution(BaseModel):
    __tablename__ = "workflow_execution"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organization.id"), nullable=False
    )
    workflow_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("workflow.id"), nullable=False
    )
    ai_employee_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("ai_employee.id"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(50), default="pending")
    trigger_type: Mapped[str] = mapped_column(String(50), default="manual")
    input_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    output_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    organization = relationship("Organization", back_populates="workflow_executions")
    workflow = relationship("Workflow", back_populates="executions")
    ai_employee = relationship("AIEmployee", back_populates="workflow_executions")