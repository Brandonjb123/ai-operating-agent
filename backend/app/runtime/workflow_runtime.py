import logging
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.workflow_execution import WorkflowExecution
from app.repositories.workflow_repository import WorkflowRepository
from app.repositories.workflow_execution_repository import WorkflowExecutionRepository
from .execution_context import ExecutionContext
from .executor_registry import ExecutorRegistry
from .step_result import StepResult

logger = logging.getLogger(__name__)


class WorkflowRuntime:
    """
    Menjalankan eksekusi workflow berdasarkan definition.
    """

    def __init__(
        self,
        db: Session,
        workflow_repo: WorkflowRepository,
        execution_repo: WorkflowExecutionRepository,
        registry: ExecutorRegistry,
    ) -> None:
        self.db = db
        self.workflow_repo = workflow_repo
        self.execution_repo = execution_repo
        self.registry = registry

    def run(self, execution_id: UUID) -> None:
        # 1. Ambil execution
        execution = self.execution_repo.get_by_id(execution_id)
        if not execution:
            raise ValueError("Execution not found")

        # 2. Validasi status awal
        if execution.status != "pending":
            raise ValueError(
                f"Cannot run execution in status '{execution.status}'. Must be 'pending'."
            )

        # 3. Ambil workflow
        workflow = self.workflow_repo.get_by_id(execution.workflow_id)
        if not workflow:
            raise ValueError("Workflow not found")

        # 4. Set running & mulai
        execution.status = "running"
        execution.started_at = datetime.now(timezone.utc)
        self.execution_repo.update(execution)
        self.db.commit()

        # 5. Siapkan context
        context = ExecutionContext(
            execution_id=execution.id,
            workflow_id=workflow.id,
            organization_id=execution.organization_id,
            ai_employee_id=execution.ai_employee_id,
            input_data=execution.input_data or {},
            variables=dict(execution.input_data or {}),  # input data menjadi variabel awal
        )

        # 6. Ambil steps
        definition = workflow.definition or {}
        steps = definition.get("steps", [])
        if not steps:
            # Tidak ada step, langsung completed
            execution.status = "completed"
            execution.output_data = {}
            execution.completed_at = datetime.now(timezone.utc)
            self.execution_repo.update(execution)
            self.db.commit()
            return

        # 7. Loop eksekusi
        try:
            for step in steps:
                step_id = step.get("id")
                if not step_id:
                    raise ValueError("Step missing 'id'")
                step_type = step.get("type")
                if not step_type:
                    raise ValueError(f"Step {step_id} missing 'type'")

                executor = self.registry.get(step_type)
                if not executor:
                    raise ValueError(f"Unknown step type: {step_type}")

                context.current_step_id = step_id
                result = executor.execute(step, context)

                # Simpan hasil
                context.step_results.append(result)
                if not result.success:
                    raise RuntimeError(result.error or "Step failed")

                # Update variables untuk step berikutnya
                if result.output:
                    context.variables.update(result.output)

            # Semua langkah sukses
            execution.status = "completed"
            execution.output_data = {
                "final_output": context.variables,
                "step_results": [
                    {
                        "step_id": r.step_id,
                        "success": r.success,
                        "output": r.output,
                        "error": r.error,
                        "metadata": r.metadata,
                    }
                    for r in context.step_results
                ],
            }
            execution.completed_at = datetime.now(timezone.utc)
            self.execution_repo.update(execution)
            self.db.commit()

        except Exception as e:
            # Gagal
            error_message = str(e)
            logger.error(
                f"Execution {execution_id} failed: {error_message}", exc_info=True
            )
            execution.status = "failed"
            execution.error_message = error_message  # pesan aman
            execution.completed_at = datetime.now(timezone.utc)
            self.execution_repo.update(execution)
            self.db.commit()