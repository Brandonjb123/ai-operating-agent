export type KnowledgeType = "document" | "faq" | "manual" | "policy" | "note";
export type KnowledgeStatus = "active" | "inactive" | "archived";

export interface Knowledge {
  id: string;
  organization_id: string;
  ai_employee_id: string;
  title: string;
  content: string;
  source: string;
  knowledge_type: KnowledgeType;
  status: KnowledgeStatus;
  metadata: Record<string, unknown> | null;
  created_at: string;
  updated_at: string;
}

export interface CreateKnowledgeRequest {
  ai_employee_id: string;
  title: string;
  content: string;
  source: string;
  knowledge_type: KnowledgeType;
  status: KnowledgeStatus;
  metadata?: Record<string, unknown> | null;
}

export interface UpdateKnowledgeRequest {
  title?: string;
  content?: string;
  source?: string;
  knowledge_type?: KnowledgeType;
  status?: KnowledgeStatus;
  metadata?: Record<string, unknown> | null;
}