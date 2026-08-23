import { apiClient } from "@/lib/api";
import type {
  Knowledge,
  CreateKnowledgeRequest,
  UpdateKnowledgeRequest,
} from "@/types/knowledge";

export async function listKnowledge(aiEmployeeId: string): Promise<Knowledge[]> {
  return apiClient<Knowledge[]>(`/knowledges/?ai_employee_id=${aiEmployeeId}`);
}

export async function getKnowledge(id: string): Promise<Knowledge> {
  return apiClient<Knowledge>(`/knowledges/${id}`);
}

export async function createKnowledge(
  payload: CreateKnowledgeRequest
): Promise<Knowledge> {
  return apiClient<Knowledge>("/knowledges/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function updateKnowledge(
  id: string,
  payload: UpdateKnowledgeRequest
): Promise<Knowledge> {
  return apiClient<Knowledge>(`/knowledges/${id}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export async function deleteKnowledge(id: string): Promise<void> {
  return apiClient<void>(`/knowledges/${id}`, {
    method: "DELETE",
  });
}