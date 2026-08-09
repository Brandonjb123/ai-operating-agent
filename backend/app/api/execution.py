from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.repositories.workflow_repository import WorkflowRepository
from app.repositories.workflow_execution_repository import WorkflowExecutionRepository
from app.runtime.workflow_runtime import WorkflowRuntime
from app.runtime.executor_registry import ExecutorRegistry
from app.runtime.executors.llm_executor import LLMExecutor
from app.ai.providers.groq_provider import GroqProvider
from app.schemas.workflow_execution import WorkflowExecutionResponse
from app.schemas.workflow_execution import RunExecutionRequest
from app.ai.providers.mock_provider import MockLLMProvider

router = APIRouter(prefix="/executions", tags=["Executions"])


@router.post("/run", response_model=WorkflowExecutionResponse)
def run_execution(
    request: RunExecutionRequest,
    db: Session = Depends(get_db),
):
    execution_id = request.execution_id
    # 1. Siapkan repository & registry
    workflow_repo = WorkflowRepository(db)
    execution_repo = WorkflowExecutionRepository(db)
    registry = ExecutorRegistry()

    # 2. Setup LLM executor dengan GroqProvider
    groq_provider = GroqProvider()  # ambil API key dari environment
    llm_executor = LLMExecutor(groq_provider)
    registry.register("llm", llm_executor)

    # 3. Buat runtime
    runtime = WorkflowRuntime(db, workflow_repo, execution_repo, registry)

    # 4. Jalankan (synchronous)
    try:
        runtime.run(execution_id)
    except ValueError as e:
        msg = str(e).lower()
        if "not found" in msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        if "cannot run" in msg or "invalid" in msg:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Execution failed")
    except Exception as e:
        # Jangan bocorkan traceback
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Execution failed")

    # 5. Ambil hasil akhir
    execution = execution_repo.get_by_id(execution_id)
    return WorkflowExecutionResponse.model_validate(execution)