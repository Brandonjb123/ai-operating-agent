"""Read-only aggregate queries for the organization dashboard."""

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.ai_employee import AIEmployee
from app.models.knowledge import Knowledge
from app.models.memory import Memory
from app.models.workflow import Workflow


class DashboardRepository:
    """Provides database-side, organization-scoped dashboard aggregates."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_summary(self, organization_id: UUID) -> dict[str, int]:
        """Return all dashboard counts in one aggregate database statement."""
        total_employees = (
            select(func.count(AIEmployee.id))
            .where(AIEmployee.organization_id == organization_id)
            .scalar_subquery()
        )
        active_employees = (
            select(func.count(AIEmployee.id))
            .where(AIEmployee.organization_id == organization_id)
            .where(AIEmployee.status == "active")
            .scalar_subquery()
        )
        total_knowledge = (
            select(func.count(Knowledge.id))
            .where(Knowledge.organization_id == organization_id)
            .scalar_subquery()
        )
        total_memory = (
            select(func.count(Memory.id))
            .where(Memory.organization_id == organization_id)
            .scalar_subquery()
        )
        total_workflows = (
            select(func.count(Workflow.id))
            .where(Workflow.organization_id == organization_id)
            .scalar_subquery()
        )

        statement = select(
            total_employees.label("total_digital_employees"),
            active_employees.label("active_digital_employees"),
            total_knowledge.label("total_knowledge"),
            total_memory.label("total_memory"),
            total_workflows.label("total_workflows"),
        )
        result = self.db.execute(statement).mappings().one()
        return {key: int(value) for key, value in result.items()}
