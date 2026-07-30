from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base_model import BaseModel
from uuid import UUID


class Role(BaseModel):
    __tablename__ = "role"

    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organization.id")
    )

    name: Mapped[str] = mapped_column(String(100))

    description: Mapped[str | None] = mapped_column(Text)