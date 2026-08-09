"""
Workflow Service — logika bisnis untuk manajemen workflow.
Menggunakan WorkflowRepository & AIEmployeeRepository.
"""

from uuid import UUID
from app.models.workflow import Workflow
from app.repositories.workflow_repository import WorkflowRepository
from app.repositories.ai_employee_repository import AIEmployeeRepository
from app.schemas.workflow import (
    WorkflowCreateRequest,
    WorkflowUpdateRequest,
    WorkflowResponse,
    ALLOWED_TRIGGER_TYPES,
    ALLOWED_STATUSES,
)


class WorkflowService:
    """Service untuk mengelola workflow."""

    def __init__(self, workflow_repo: WorkflowRepository, ai_employee_repo: AIEmployeeRepository) -> None:
        self.workflow_repo = workflow_repo
        self.ai_employee_repo = ai_employee_repo

    def list_workflows(self, ai_employee_id: UUID) -> list[WorkflowResponse]:
        """Mendaftar semua workflow milik AI employee tertentu."""
        workflows = self.workflow_repo.list_by_ai_employee(ai_employee_id)
        return [WorkflowResponse.model_validate(w) for w in workflows]

    def get_workflow(self, workflow_id: UUID) -> WorkflowResponse:
        """Mendapatkan workflow berdasarkan ID."""
        workflow = self.workflow_repo.get_by_id(workflow_id)
        if workflow is None:
            raise ValueError("Workflow not found")
        return WorkflowResponse.model_validate(workflow)

    def create_workflow(self, request: WorkflowCreateRequest) -> WorkflowResponse:
        """Membuat workflow baru dengan berbagai aturan bisnis."""
        # 1. Pastikan AI employee ada
        ai_employee = self.ai_employee_repo.get_by_id(request.ai_employee_id)
        if ai_employee is None:
            raise ValueError("AI employee not found")

        # 2. Validasi name
        name = request.name.strip()
        if not name:
            raise ValueError("Workflow name is required")

        # 3. Cek duplikasi nama dalam AI employee yang sama
        existing = self.workflow_repo.get_by_name(request.ai_employee_id, name)
        if existing:
            raise ValueError("Workflow with this name already exists for this AI employee")

        # 4. Validasi definition
        if not request.definition:
            raise ValueError("Workflow definition is required")

        # 5. Validasi trigger_type (sudah di schema, double check)
        if request.trigger_type.lower() not in ALLOWED_TRIGGER_TYPES:
            raise ValueError(f"Unsupported trigger type '{request.trigger_type}'")

        # 6. Validasi status
        if request.status.lower() not in ALLOWED_STATUSES:
            raise ValueError(f"Invalid status '{request.status}'")

        # Buat objek Workflow
        workflow = Workflow(
            organization_id=ai_employee.organization_id,
            ai_employee_id=request.ai_employee_id,
            name=name,
            description=request.description,
            definition=request.definition,
            trigger_type=request.trigger_type.lower(),
            status=request.status.lower(),
        )
        saved = self.workflow_repo.create(workflow)
        return WorkflowResponse.model_validate(saved)

    def update_workflow(
        self, workflow_id: UUID, request: WorkflowUpdateRequest
    ) -> WorkflowResponse:
        """Memperbarui workflow. Hanya field yang tidak None yang diupdate."""
        workflow = self.workflow_repo.get_by_id(workflow_id)
        if workflow is None:
            raise ValueError("Workflow not found")

        if request.name is not None:
            new_name = request.name.strip()
            if not new_name:
                raise ValueError("Workflow name is required")
            existing = self.workflow_repo.get_by_name(workflow.ai_employee_id, new_name)
            if existing and existing.id != workflow_id:
                raise ValueError("Workflow with this name already exists for this AI employee")
            workflow.name = new_name

        if request.description is not None:
            workflow.description = request.description

        if request.definition is not None:
            if not request.definition:
                raise ValueError("Workflow definition is required")
            workflow.definition = request.definition

        if request.trigger_type is not None:
            if request.trigger_type.lower() not in ALLOWED_TRIGGER_TYPES:
                raise ValueError(f"Unsupported trigger type '{request.trigger_type}'")
            workflow.trigger_type = request.trigger_type.lower()

        if request.status is not None:
            if request.status.lower() not in ALLOWED_STATUSES:
                raise ValueError(f"Invalid status '{request.status}'")
            workflow.status = request.status.lower()

        updated = self.workflow_repo.update(workflow)
        return WorkflowResponse.model_validate(updated)

    def delete_workflow(self, workflow_id: UUID) -> None:
        """Menghapus workflow berdasarkan ID."""
        workflow = self.workflow_repo.get_by_id(workflow_id)
        if workflow is None:
            raise ValueError("Workflow not found")
        self.workflow_repo.delete(workflow)