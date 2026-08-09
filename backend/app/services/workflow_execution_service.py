"""
Workflow Execution Service — logika bisnis untuk manajemen eksekusi workflow.
Menggunakan WorkflowExecutionRepository, WorkflowRepository, dan AIEmployeeRepository.
"""

from uuid import UUID
from app.models.workflow_execution import WorkflowExecution
from app.repositories.workflow_execution_repository import WorkflowExecutionRepository
from app.repositories.workflow_repository import WorkflowRepository
from app.repositories.ai_employee_repository import AIEmployeeRepository
from app.schemas.workflow_execution import (
    WorkflowExecutionCreateRequest,
    WorkflowExecutionUpdateRequest,
    WorkflowExecutionResponse,
    ALLOWED_EXECUTION_STATUSES,
    ALLOWED_TRIGGER_TYPES,
)


class WorkflowExecutionService:
    """Service untuk mengelola eksekusi workflow (hanya data, bukan runtime)."""

    def __init__(
        self,
        execution_repo: WorkflowExecutionRepository,
        workflow_repo: WorkflowRepository,
        ai_employee_repo: AIEmployeeRepository,
    ) -> None:
        self.execution_repo = execution_repo
        self.workflow_repo = workflow_repo
        self.ai_employee_repo = ai_employee_repo

    # ----- Read operations -----
    def list_executions_by_workflow(self, workflow_id: UUID) -> list[WorkflowExecutionResponse]:
        executions = self.execution_repo.list_by_workflow(workflow_id)
        return [WorkflowExecutionResponse.model_validate(e) for e in executions]

    def list_executions_by_ai_employee(self, ai_employee_id: UUID) -> list[WorkflowExecutionResponse]:
        executions = self.execution_repo.list_by_ai_employee(ai_employee_id)
        return [WorkflowExecutionResponse.model_validate(e) for e in executions]

    def list_executions_by_organization(self, organization_id: UUID) -> list[WorkflowExecutionResponse]:
        executions = self.execution_repo.list_by_organization(organization_id)
        return [WorkflowExecutionResponse.model_validate(e) for e in executions]

    def get_execution(self, execution_id: UUID) -> WorkflowExecutionResponse:
        execution = self.execution_repo.get_by_id(execution_id)
        if execution is None:
            raise ValueError("Execution not found")
        return WorkflowExecutionResponse.model_validate(execution)

    # ----- Create -----
    def create_execution(self, request: WorkflowExecutionCreateRequest) -> WorkflowExecutionResponse:
        # 1. Validasi workflow
        workflow = self.workflow_repo.get_by_id(request.workflow_id)
        if workflow is None:
            raise ValueError("Workflow not found")

        # 2. Validasi AI Employee
        ai_employee = self.ai_employee_repo.get_by_id(request.ai_employee_id)
        if ai_employee is None:
            raise ValueError("AI employee not found")

        # 3. Konsistensi: workflow dan AI employee harus terkait
        if workflow.ai_employee_id != request.ai_employee_id:
            raise ValueError("Workflow does not belong to this AI employee")

        # 4. Organisasi harus konsisten
        if workflow.organization_id != ai_employee.organization_id:
            raise ValueError("Workflow and AI employee are in different organizations")

        # 5. Workflow harus aktif
        if workflow.status != "active":
            raise ValueError("Cannot create execution for an inactive workflow")

        # 6. Trigger type valid (sudah divalidasi schema, tapi double-check)
        if request.trigger_type.lower() not in ALLOWED_TRIGGER_TYPES:
            raise ValueError(f"Unsupported trigger type '{request.trigger_type}'")

        # 7. Initial status selalu pending
        status = "pending"

        # Buat objek execution
        execution = WorkflowExecution(
            organization_id=workflow.organization_id,
            workflow_id=request.workflow_id,
            ai_employee_id=request.ai_employee_id,
            status=status,
            trigger_type=request.trigger_type.lower(),
            input_data=request.input_data or {},
            output_data=None,
            error_message=None,
            started_at=None,
            completed_at=None,
        )
        saved = self.execution_repo.create(execution)
        return WorkflowExecutionResponse.model_validate(saved)

    # ----- Update -----
    def update_execution(
        self, execution_id: UUID, request: WorkflowExecutionUpdateRequest
    ) -> WorkflowExecutionResponse:
        execution = self.execution_repo.get_by_id(execution_id)
        if execution is None:
            raise ValueError("Execution not found")

        # Update field yang diberikan (tanpa otomatisasi transisi)
        if request.status is not None:
            if request.status.lower() not in ALLOWED_EXECUTION_STATUSES:
                raise ValueError(f"Invalid status '{request.status}'")
            execution.status = request.status.lower()

        if request.input_data is not None:
            execution.input_data = request.input_data

        if request.output_data is not None:
            execution.output_data = request.output_data

        if request.error_message is not None:
            execution.error_message = request.error_message

        if request.started_at is not None:
            execution.started_at = request.started_at

        if request.completed_at is not None:
            execution.completed_at = request.completed_at

        updated = self.execution_repo.update(execution)
        return WorkflowExecutionResponse.model_validate(updated)

    # ----- Delete -----
    def delete_execution(self, execution_id: UUID) -> None:
        execution = self.execution_repo.get_by_id(execution_id)
        if execution is None:
            raise ValueError("Execution not found")
        self.execution_repo.delete(execution)