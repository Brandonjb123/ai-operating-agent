from dataclasses import dataclass, field
from uuid import UUID

@dataclass
class ExecutionContext:
    execution_id: UUID
    workflow_id: UUID
    organization_id: UUID
    ai_employee_id: UUID
    input_data: dict = field(default_factory=dict)
    variables: dict = field(default_factory=dict)
    current_step_id: str | None = None
    step_results: list = field(default_factory=list)