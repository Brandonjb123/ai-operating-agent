import { apiClient } from "@/lib/api";
import type {
  Workflow,
  CreateWorkflowRequest,
  UpdateWorkflowRequest,
} from "@/types/workflow";

export async function listWorkflows(aiEmployeeId: string): Promise<Workflow[]> {
  return apiClient<Workflow[]>(`/workflows/?ai_employee_id=${aiEmployeeId}`);
}

export async function getWorkflow(id: string): Promise<Workflow> {
  return apiClient<Workflow>(`/workflows/${id}`);
}

export async function createWorkflow(
  payload: CreateWorkflowRequest
): Promise<Workflow> {
  return apiClient<Workflow>("/workflows/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function updateWorkflow(
  id: string,
  payload: UpdateWorkflowRequest
): Promise<Workflow> {
  return apiClient<Workflow>(`/workflows/${id}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export async function deleteWorkflow(id: string): Promise<void> {
  return apiClient<void>(`/workflows/${id}`, {
    method: "DELETE",
  });
}