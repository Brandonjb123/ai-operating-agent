from dataclasses import dataclass, field
from uuid import UUID
from .step_result import StepResult


@dataclass
class ExecutionContext:
    execution_id: UUID
    workflow_id: UUID
    organization_id: UUID
    ai_employee_id: UUID
    input_data: dict = field(default_factory=dict)
    variables: dict = field(default_factory=dict)
    current_step_id: str | None = None
    step_results: list[StepResult] = field(default_factory=list)

    def set_current_step(self, step_id: str) -> None:
        self.current_step_id = step_id

    def add_step_result(self, result: StepResult) -> None:
        self.step_results.append(result)

    def update_variables(self, data: dict) -> None:
        if data:
            self.variables.update(data)

    def get_step_results(self) -> list[StepResult]:
        return self.step_results