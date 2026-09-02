"""Dashboard API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.dependencies.database import get_db
from app.models.user import User
from app.repositories.dashboard_repository import DashboardRepository
from app.repositories.membership_repository import MembershipRepository
from app.schemas.dashboard import DashboardSummaryResponse
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


def get_dashboard_service(db: Session = Depends(get_db)) -> DashboardService:
    """Build the dashboard service with request-scoped repositories."""
    return DashboardService(
        dashboard_repository=DashboardRepository(db),
        membership_repository=MembershipRepository(db),
    )


@router.get("/summary", response_model=DashboardSummaryResponse)
def get_dashboard_summary(
    organization_id: UUID = Query(..., description="UUID organisasi"),
    current_user: User = Depends(get_current_user),
    service: DashboardService = Depends(get_dashboard_service),
) -> DashboardSummaryResponse:
    """Return aggregate metrics for an organization the caller belongs to."""
    try:
        return service.get_summary(organization_id, current_user)
    except PermissionError as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(error),
        ) from error
