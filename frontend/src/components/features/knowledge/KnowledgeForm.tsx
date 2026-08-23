"use client";

import React, { useState } from "react";
import KnowledgeTypeSelect from "./KnowledgeTypeSelect";
import KnowledgeStatusSelect from "./KnowledgeStatusSelect";
import { getErrorMessage } from "@/lib/error";
import type { AIEmployee } from "@/types/digital-employee";
import type {
  KnowledgeType,
  KnowledgeStatus,
} from "@/types/knowledge";

export interface KnowledgeFormValues {
  ai_employee_id: string;
  title: string;
  content: string;
  source: string;
  knowledge_type: KnowledgeType;
  status: KnowledgeStatus;
  metadata: Record<string, unknown> | null;
}

interface KnowledgeFormProps {
  employees: AIEmployee[];
  initialValues?: Partial<KnowledgeFormValues>;
  onSubmit: (values: KnowledgeFormValues) => Promise<void>;
  submitLabel: string;
  disableEmployeeSelect?: boolean;
}

export default function KnowledgeForm({
  employees,
  initialValues = {},
  onSubmit,
  submitLabel,
  disableEmployeeSelect = false,
}: KnowledgeFormProps) {
  const [aiEmployeeId, setAiEmployeeId] = useState(
    initialValues.ai_employee_id || ""
  );
  const [title, setTitle] = useState(initialValues.title || "");
  const [content, setContent] = useState(initialValues.content || "");
  const [source, setSource] = useState(initialValues.source || "");
  const [knowledgeType, setKnowledgeType] = useState<KnowledgeType>(
    initialValues.knowledge_type || "document"
  );
  const [status, setStatus] = useState<KnowledgeStatus>(
    initialValues.status || "active"
  );
  const [metadataText, setMetadataText] = useState(() => {
    if (initialValues.metadata) {
      return JSON.stringify(initialValues.metadata, null, 2);
    }
    return "";
  });
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);

    if (!aiEmployeeId) {
      setError("Digital Employee is required");
      return;
    }
    if (!title.trim()) {
      setError("Title is required");
      return;
    }
    if (!content.trim()) {
      setError("Content is required");
      return;
    }
    if (!source.trim()) {
      setError("Source is required");
      return;
    }

    let metadata: Record<string, unknown> | null = null;
    if (metadataText.trim()) {
      try {
        metadata = JSON.parse(metadataText);
      } catch {
        setError("Metadata must be valid JSON");
        return;
      }
    }

    setSubmitting(true);
    try {
      await onSubmit({
        ai_employee_id: aiEmployeeId,
        title: title.trim(),
        content: content.trim(),
        source: source.trim(),
        knowledge_type: knowledgeType,
        status,
        metadata,
      });
    } catch (err) {
      setError(getErrorMessage(err, "Submit failed"));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="max-w-3xl space-y-6">
      {error && (
        <div className="rounded-md bg-red-50 p-4">
          <p className="text-sm text-red-700">{error}</p>
        </div>
      )}

      <div>
        <label className="block text-sm font-medium text-gray-700">
          Digital Employee *
        </label>
        <select
          value={aiEmployeeId}
          onChange={(e) => setAiEmployeeId(e.target.value)}
          disabled={disableEmployeeSelect}
          className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 disabled:bg-gray-100 disabled:text-gray-500"
        >
          <option value="">Select Digital Employee</option>
          {employees.map((emp) => (
            <option key={emp.id} value={emp.id}>
              {emp.name}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">
          Title *
        </label>
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">
          Content *
        </label>
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          rows={6}
          className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">
          Source *
        </label>
        <input
          type="text"
          value={source}
          onChange={(e) => setSource(e.target.value)}
          className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
          required
        />
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div>
          <label className="block text-sm font-medium text-gray-700">
            Knowledge Type
          </label>
          <KnowledgeTypeSelect
            value={knowledgeType}
            onChange={setKnowledgeType}
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">
            Status
          </label>
          <KnowledgeStatusSelect value={status} onChange={setStatus} />
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">
          Metadata (JSON, opsional)
        </label>
        <textarea
          value={metadataText}
          onChange={(e) => setMetadataText(e.target.value)}
          rows={4}
          className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 font-mono text-sm"
          placeholder='{"author":"Brandon"}'
        />
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