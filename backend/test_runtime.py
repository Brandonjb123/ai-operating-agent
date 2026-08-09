import uuid
from app.database.database import SessionLocal
from app.repositories.workflow_repository import WorkflowRepository
from app.repositories.workflow_execution_repository import WorkflowExecutionRepository
from app.runtime.executor_registry import ExecutorRegistry
from app.runtime.executors.llm_executor import LLMExecutor
from app.ai.providers.mock_provider import MockLLMProvider
from app.runtime.workflow_runtime import WorkflowRuntime
from app.models.workflow_execution import WorkflowExecution

# Setup mock
db = SessionLocal()
workflow_repo = WorkflowRepository(db)
execution_repo = WorkflowExecutionRepository(db)
registry = ExecutorRegistry()

mock_llm = MockLLMProvider()
llm_executor = LLMExecutor(mock_llm)
registry.register("llm", llm_executor)

runtime = WorkflowRuntime(db, workflow_repo, execution_repo, registry)

# Buat execution baru (pending)
workflow_id = uuid.UUID("2ab62025-a34b-4bba-83d0-3fae92776ba5")  # workflow yang sama
ai_employee_id = uuid.UUID("42c0994e-4498-428b-a4ce-e4a4854e00c6")
organization_id = uuid.UUID("b418fbc1-3ddb-467c-85ef-ae69d64509b2")

execution = WorkflowExecution(
    organization_id=organization_id,
    workflow_id=workflow_id,
    ai_employee_id=ai_employee_id,
    status="pending",
    trigger_type="manual",
    input_data={},
)
db.add(execution)
db.commit()
db.refresh(execution)
execution_id = execution.id
print(f"Created execution: {execution_id}")

# Jalankan runtime
try:
    runtime.run(execution_id)
    print("Runtime finished.")
except Exception as e:
    print(f"Runtime error: {e}")
finally:
    db.close()

# Verifikasi hasil
db2 = SessionLocal()
execution_repo2 = WorkflowExecutionRepository(db2)
exec2 = execution_repo2.get_by_id(execution_id)
if exec2:
    print(f"Status: {exec2.status}")
    print(f"Output: {exec2.output_data}")
    print(f"Error: {exec2.error_message}")
    print(f"Started: {exec2.started_at}")
    print(f"Completed: {exec2.completed_at}")
db2.close()