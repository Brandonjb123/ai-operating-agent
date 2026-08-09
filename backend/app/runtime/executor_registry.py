from .step_executor import StepExecutor

class ExecutorRegistry:
    def __init__(self):
        self._executors: dict[str, StepExecutor] = {}

    def register(self, step_type: str, executor: StepExecutor):
        self._executors[step_type] = executor

    def get(self, step_type: str) -> StepExecutor | None:
        return self._executors.get(step_type)