from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base_model import BaseModel
from uuid import UUID

class Organization(BaseModel):
    __tablename__ = "organization"

    name: Mapped[str] = mapped_column(String(255))

    slug: Mapped[str] = mapped_column(
        String(255),
        unique=True,
    )

    description: Mapped[str | None] = mapped_column(Text)

    logo_url: Mapped[str | None]

    website: Mapped[str | None]

    status: Mapped[str]

    ai_employees = relationship("AIEmployee", back_populates="organization")