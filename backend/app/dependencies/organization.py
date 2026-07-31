"""
Sementara: menyediakan default organization_id agar user bisa didaftarkan
tanpa menyertakan organization di request body.
Akan diganti dengan mekanisme context organization yang sesungguhnya.
"""

from uuid import UUID
from fastapi import Depends
from sqlalchemy.orm import Session
from app.models.organization import Organization
from app.dependencies.database import get_db


def get_default_organization_id(db: Session = Depends(get_db)) -> UUID:
    """
    Mengambil ID organisasi default (yang pertama di database).
    Jika belum ada organisasi sama sekali, buat satu dengan slug='default'.
    """
    org = db.query(Organization).first()
    if not org:
        org = Organization(
            name="Default Organization",
            slug="default",
            status="active"
        )
        db.add(org)
        db.commit()
        db.refresh(org)
    return org.id