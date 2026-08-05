"""
Memory Model — penyimpanan informasi jangka panjang untuk AI Employee.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Text, Integer, ForeignKey, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base_model import BaseModel


class Memory(BaseModel):
    __tablename__ = "memory"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organization.id"), nullable=False
    )
    ai_employee_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("ai_employee.id"), nullable=False
    )
    memory_key: Mapped[str] = mapped_column(String(255), nullable=False)
    memory_value: Mapped[str] = mapped_column(Text, nullable=False)
    memory_type: Mapped[str] = mapped_column(String(50), default="long_term")
    importance: Mapped[int] = mapped_column(Integer, default=1)
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSON, nullable=True)
    last_accessed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    organization = relationship("Organization", back_populates="memories")
    ai_employee = relationship("AIEmployee", back_populates="memories")