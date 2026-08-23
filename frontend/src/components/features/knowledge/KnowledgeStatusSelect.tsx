"use client";

import type { KnowledgeStatus } from "@/types/knowledge";

interface Props {
  value: KnowledgeStatus;
  onChange: (value: KnowledgeStatus) => void;
  disabled?: boolean;
}

const statuses: KnowledgeStatus[] = ["active", "inactive", "archived"];

export default function KnowledgeStatusSelect({ value, onChange, disabled }: Props) {
  return (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value as KnowledgeStatus)}
      disabled={disabled}
      className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 disabled:bg-gray-100 disabled:text-gray-500"
    >
      {statuses.map((s) => (
        <option key={s} value={s}>
          {s}
        </option>
      ))}
    </select>
  );
}