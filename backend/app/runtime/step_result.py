from dataclasses import dataclass, field
from uuid import UUID

@dataclass
class StepResult:
    step_id: str
    success: bool
    output: dict | None = None
    error: str | None = None
    metadata: dict = field(default_factory=dict)