"use client";

import React, { useState } from "react";
import WorkflowStepEditor from "./WorkflowStepEditor";
import { getErrorMessage } from "@/lib/error";
import type { AIEmployee } from "@/types/digital-employee";
import type {
  WorkflowStep,
  WorkflowTriggerType,
  WorkflowStatus,
} from "@/types/workflow";

export interface WorkflowFormValues {
  ai_employee_id: string;
  name: string;
  description: string | null;
  trigger_type: WorkflowTriggerType;
  status: WorkflowStatus;
  steps: WorkflowStep[];
}

interface WorkflowFormProps {
  employees: AIEmployee[];
  initialValues?: Partial<WorkflowFormValues>;
  onSubmit: (values: WorkflowFormValues) => Promise<void>;
  submitLabel: string;
  disableEmployeeSelect?: boolean;
}

export default function WorkflowForm({
  employees,
  initialValues = {},
  onSubmit,
  submitLabel,
  disableEmployeeSelect = false,
}: WorkflowFormProps) {
  const [aiEmployeeId, setAiEmployeeId] = useState(
    initialValues.ai_employee_id || ""
  );
  const [name, setName] = useState(initialValues.name || "");
  const [description, setDescription] = useState(
    initialValues.description || ""
  );
  const [triggerType, setTriggerType] = useState<WorkflowTriggerType>(
    initialValues.trigger_type || "manual"
  );
  const [status, setStatus] = useState<WorkflowStatus>(
    initialValues.status || "active"
  );
  const [steps, setSteps] = useState<WorkflowStep[]>(
    initialValues.steps || []
  );
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);

    if (!aiEmployeeId) {
      setError("Digital Employee is required");
      return;
    }
    if (!name.trim()) {
      setError("Name is required");
      return;
    }
    for (let i = 0; i < steps.length; i++) {
      if (!steps[i].config.prompt.trim()) {
        setError(`Prompt for Step ${i + 1} is required`);
        return;
      }
    }

    setSubmitting(true);
    try {
      await onSubmit({
        ai_employee_id: aiEmployeeId,
        name: name.trim(),
        description: description || null,
        trigger_type: triggerType,
        status,
        steps,
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
          Name *
        </label>
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
          rows={3}
          className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
        />
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div>
          <label className="block text-sm font-medium text-gray-700">
            Trigger Type
          </label>
          <select
            value={triggerType}
            onChange={(e) =>
              setTriggerType(e.target.value as WorkflowTriggerType)
            }
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
          >
            <option value="manual">manual</option>
            <option value="api">api</option>
            <option value="schedule">schedule</option>
            <option value="event">event</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">
            Status
          </label>
          <select
            value={status}
            onChange={(e) => setStatus(e.target.value as WorkflowStatus)}
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
          >
            <option value="active">active</option>
            <option value="inactive">inactive</option>
          </select>
        </div>
      </div>

      <WorkflowStepEditor steps={steps} onChange={setSteps} />

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