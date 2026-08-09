"""
Workflow Model — definisi proses yang dimiliki AI Employee.
"""

import uuid
from sqlalchemy import String, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base_model import BaseModel


class Workflow(BaseModel):
    __tablename__ = "workflow"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organization.id"), nullable=False
    )
    ai_employee_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("ai_employee.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    definition: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(50), default="active")
    trigger_type: Mapped[str] = mapped_column(String(50), default="manual")

    # Relationships
    organization = relationship("Organization", back_populates="workflows")
    ai_employee = relationship("AIEmployee", back_populates="workflows")