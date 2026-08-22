import { apiClient } from "@/lib/api";
import type {
  AIEmployee,
  CreateDigitalEmployeeRequest,
  UpdateDigitalEmployeeRequest,
} from "@/types/digital-employee";

export async function listDigitalEmployees(
  organizationId: string
): Promise<AIEmployee[]> {
  return apiClient<AIEmployee[]>(`/agents/?organization_id=${organizationId}`);
}

export async function getDigitalEmployee(id: string): Promise<AIEmployee> {
  return apiClient<AIEmployee>(`/agents/${id}`);
}

export async function createDigitalEmployee(
  payload: CreateDigitalEmployeeRequest
): Promise<AIEmployee> {
  return apiClient<AIEmployee>("/agents/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function updateDigitalEmployee(
  id: string,
  payload: UpdateDigitalEmployeeRequest
): Promise<AIEmployee> {
  return apiClient<AIEmployee>(`/agents/${id}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export async function deleteDigitalEmployee(id: string): Promise<void> {
  return apiClient<void>(`/agents/${id}`, {
    method: "DELETE",
  });
}