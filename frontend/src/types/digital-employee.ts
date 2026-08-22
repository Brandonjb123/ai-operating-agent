export type Provider = "groq" | "openai" | "anthropic" | "google" | "ollama";
export type Status = "active" | "inactive";

export interface AIEmployee {
  id: string;
  organization_id: string;
  name: string;
  description: string | null;
  avatar_url: string | null;
  provider: Provider;
  model: string;
  temperature: number;
  max_tokens: number;
  system_prompt: string;
  status: Status;
  created_at: string;
  updated_at: string;
}

export interface CreateDigitalEmployeeRequest {
  organization_id: string;
  name: string;
  description?: string | null;
  avatar_url?: string | null;
  provider: Provider;
  model: string;
  temperature: number;
  max_tokens: number;
  system_prompt: string;
  status: Status;
}

export interface UpdateDigitalEmployeeRequest {
  name?: string;
  description?: string | null;
  avatar_url?: string | null;
  provider?: Provider;
  model?: string;
  temperature?: number;
  max_tokens?: number;
  system_prompt?: string;
  status?: Status;
}