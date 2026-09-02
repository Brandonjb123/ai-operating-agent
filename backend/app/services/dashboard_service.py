"""Business rules for the organization dashboard."""

from uuid import UUID

from app.models.user import User
from app.repositories.dashboard_repository import DashboardRepository
from app.repositories.membership_repository import MembershipRepository
from app.schemas.dashboard import DashboardSummaryResponse


class DashboardService:
    """Builds dashboard summaries after enforcing tenant membership."""

    def __init__(
        self,
        dashboard_repository: DashboardRepository,
        membership_repository: MembershipRepository,
    ) -> None:
        self.dashboard_repository = dashboard_repository
        self.membership_repository = membership_repository

    def get_summary(
        self, organization_id: UUID, current_user: User
    ) -> DashboardSummaryResponse:
        """Return a summary only when the user belongs to the organization."""
        membership = self.membership_repository.get_membership(
            organization_id, current_user.id
        )
        if membership is None:
            raise PermissionError("You are not a member of this organization")

        return DashboardSummaryResponse(
            **self.dashboard_repository.get_summary(organization_id)
        )
