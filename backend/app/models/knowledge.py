"""
Knowledge Model — sumber pengetahuan terstruktur untuk AI Employee.
"""

import uuid
from sqlalchemy import String, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base_model import BaseModel


class Knowledge(BaseModel):
    __tablename__ = "knowledge"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organization.id"), nullable=False
    )
    ai_employee_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("ai_employee.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[str] = mapped_column(String(100), nullable=False)
    knowledge_type: Mapped[str] = mapped_column(String(50), default="document")
    status: Mapped[str] = mapped_column(String(50), default="active")
    # Gunakan nama kolom "metadata" di database, tetapi atribut Python "metadata_"
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSON, nullable=True)

    # Relationships
    organization = relationship("Organization", back_populates="knowledges")
    ai_employee = relationship("AIEmployee", back_populates="knowledges")