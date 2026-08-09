from abc import ABC, abstractmethod
from .execution_context import ExecutionContext
from .step_result import StepResult

class StepExecutor(ABC):
    @abstractmethod
    def execute(self, step: dict, context: ExecutionContext) -> StepResult:
        ...