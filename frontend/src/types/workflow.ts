export type WorkflowTriggerType = "manual" | "api" | "schedule" | "event";
export type WorkflowStatus = "active" | "inactive";

export interface WorkflowStep {
  id: string;
  type: "llm"; // V1 hanya mendukung LLM step
  config: {
    prompt: string;
  };
}

export interface Workflow {
  id: string;
  organization_id: string;
  ai_employee_id: string;
  name: string;
  description: string | null;
  definition: {
    steps: WorkflowStep[];
  };
  trigger_type: WorkflowTriggerType;
  status: WorkflowStatus;
  created_at: string;
  updated_at: string;
}

export interface CreateWorkflowRequest {
  ai_employee_id: string;
  name: string;
  description?: string | null;
  definition: {
    steps: WorkflowStep[];
  };
  trigger_type: WorkflowTriggerType;
  status: WorkflowStatus;
}

export interface UpdateWorkflowRequest {
  name?: string;
  description?: string | null;
  definition?: {
    steps: WorkflowStep[];
  };
  trigger_type?: WorkflowTriggerType;
  status?: WorkflowStatus;
}