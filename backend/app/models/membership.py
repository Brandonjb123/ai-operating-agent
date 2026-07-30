from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base_model import BaseModel

class Membership(BaseModel):
    __tablename__ = "membership"

    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organization.id")
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id")
    )

    role_id: Mapped[UUID] = mapped_column(
        ForeignKey("role.id")
    )

    joined_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True)
    )