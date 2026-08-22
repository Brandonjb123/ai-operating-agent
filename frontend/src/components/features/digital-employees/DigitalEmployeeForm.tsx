"use client";

import React, { useState } from "react";
import ProviderSelect from "./ProviderSelect";
import { getErrorMessage } from "@/lib/error";
import type {
  Provider,
  Status,
  CreateDigitalEmployeeRequest,
  UpdateDigitalEmployeeRequest,
} from "@/types/digital-employee";

interface DigitalEmployeeFormProps {
  initialValues?: Partial<CreateDigitalEmployeeRequest>;
  onSubmit: (
    values: CreateDigitalEmployeeRequest | UpdateDigitalEmployeeRequest
  ) => Promise<void>;
  submitLabel: string;
}

export default function DigitalEmployeeForm({
  initialValues = {},
  onSubmit,
  submitLabel,
}: DigitalEmployeeFormProps) {
  const [name, setName] = useState(initialValues.name || "");
  const [description, setDescription] = useState(initialValues.description || "");
  const [avatarUrl, setAvatarUrl] = useState(initialValues.avatar_url || "");
  const [provider, setProvider] = useState<Provider>(
    initialValues.provider || "groq"
  );
  const [model, setModel] = useState(initialValues.model || "llama3-8b-8192");
  const [temperature, setTemperature] = useState<number>(
    initialValues.temperature ?? 0.7
  );
  const [maxTokens, setMaxTokens] = useState<number>(
    initialValues.max_tokens ?? 4096
  );
  const [systemPrompt, setSystemPrompt] = useState(
    initialValues.system_prompt || ""
  );
  const [status, setStatus] = useState<Status>(initialValues.status || "active");
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);

    if (!name.trim()) {
      setError("Name is required");
      return;
    }
    if (temperature < 0 || temperature > 2) {
      setError("Temperature must be between 0 and 2");
      return;
    }
    if (maxTokens <= 0) {
      setError("Max Tokens must be greater than 0");
      return;
    }
    if (!systemPrompt.trim()) {
      setError("System Prompt is required");
      return;
    }

    setSubmitting(true);
    try {
      const payload = {
        name: name.trim(),
        description: description || null,
        avatar_url: avatarUrl || null,
        provider,
        model,
        temperature,
        max_tokens: maxTokens,
        system_prompt: systemPrompt.trim(),
        status,
      };
      await onSubmit(payload);
    } catch (err) {
      setError(getErrorMessage(err, "Submit failed"));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6 max-w-2xl">
      {error && (
        <div className="rounded-md bg-red-50 p-4">
          <p className="text-sm text-red-700">{error}</p>
        </div>
      )}
      <div>
        <label className="block text-sm font-medium text-gray-700">Name *</label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
          required
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700">
          Description
        </label>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
          rows={3}
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700">
          Avatar URL
        </label>
        <input
          type="url"
          value={avatarUrl}
          onChange={(e) => setAvatarUrl(e.target.value)}
          className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
        />
      </div>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div>
          <label className="block text-sm font-medium text-gray-700">
            Provider *
          </label>
          <ProviderSelect value={provider} onChange={setProvider} />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">
            Model *
          </label>
          <input
            type="text"
            value={model}
            onChange={(e) => setModel(e.target.value)}
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
            required
          />
        </div>
      </div>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div>
          <label className="block text-sm font-medium text-gray-700">
            Temperature (0-2) *
          </label>
          <input
            type="number"
            step="0.1"
            min={0}
            max={2}
            value={temperature}
            onChange={(e) => setTemperature(parseFloat(e.target.value))}
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">
            Max Tokens *
          </label>
          <input
            type="number"
            min={1}
            value={maxTokens}
            onChange={(e) => setMaxTokens(parseInt(e.target.value, 10))}
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
            required
          />
        </div>
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700">
          System Prompt *
        </label>
        <textarea
          value={systemPrompt}
          onChange={(e) => setSystemPrompt(e.target.value)}
          className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
          rows={4}
          required
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700">Status *</label>
        <select
          value={status}
          onChange={(e) => setStatus(e.target.value as Status)}
          className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
        >
          <option value="active">active</option>
          <option value="inactive">inactive</option>
        </select>
      </div>
      <button
        type="submit"
        disabled={submitting}
        className="inline-flex justify-center rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
      >
        {submitting ? "Saving..." : submitLabel}
      </button>
    </form>
  );
}