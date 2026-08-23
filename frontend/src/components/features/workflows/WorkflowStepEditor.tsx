"use client";

import { WorkflowStep } from "@/types/workflow";

interface WorkflowStepEditorProps {
  steps: WorkflowStep[];
  onChange: (steps: WorkflowStep[]) => void;
}

function generateStepId() {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) {
    return crypto.randomUUID();
  }
  return `step_${Date.now()}`;
}

export default function WorkflowStepEditor({
  steps,
  onChange,
}: WorkflowStepEditorProps) {
  function addStep() {
    const newStep: WorkflowStep = {
      id: generateStepId(),
      type: "llm",
      config: { prompt: "" },
    };
    onChange([...steps, newStep]);
  }

  function removeStep(index: number) {
    const next = steps.filter((_, i) => i !== index);
    onChange(next);
  }

  function updatePrompt(index: number, prompt: string) {
    const next = steps.map((step, i) =>
      i === index ? { ...step, config: { ...step.config, prompt } } : step
    );
    onChange(next);
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-medium text-gray-700">Steps</h3>
        <button
          type="button"
          onClick={addStep}
          className="rounded-md bg-gray-100 px-3 py-1.5 text-sm font-medium text-gray-700 hover:bg-gray-200"
        >
          Add LLM Step
        </button>
      </div>

      {steps.length === 0 && (
        <p className="text-sm text-gray-500">
          No steps yet. Click “Add LLM Step” to start.
        </p>
      )}

      {steps.map((step, index) => (
        <div
          key={step.id}
          className="rounded-md border border-gray-200 bg-gray-50 p-4"
        >
          <div className="mb-2 flex items-center justify-between">
            <span className="text-xs font-semibold uppercase text-gray-500">
              Step {index + 1} — LLM
            </span>
            <button
              type="button"
              onClick={() => removeStep(index)}
              className="text-sm text-red-600 hover:text-red-900"
            >
              Remove
            </button>
          </div>
          <label className="block text-sm font-medium text-gray-700">
            Prompt *
          </label>
          <textarea
            value={step.config.prompt}
            onChange={(e) => updatePrompt(index, e.target.value)}
            rows={3}
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
            placeholder="Enter prompt for this LLM step"
          />
        </div>
      ))}
    </div>
  );
}