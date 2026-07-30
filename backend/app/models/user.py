from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base_model import BaseModel

class User(BaseModel):
    __tablename__ = "user"

    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organization.id")
    )

    last_login: Mapped[datetime | None]

    full_name: Mapped[str] = mapped_column(String(255))

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
    )

    password_hash: Mapped[str]

    avatar_url: Mapped[str | None]

    status: Mapped[str]

    last_login: Mapped[datetime | None]