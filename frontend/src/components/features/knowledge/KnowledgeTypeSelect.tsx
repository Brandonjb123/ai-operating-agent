"use client";

import type { KnowledgeType } from "@/types/knowledge";

interface Props {
  value: KnowledgeType;
  onChange: (value: KnowledgeType) => void;
  disabled?: boolean;
}

const types: KnowledgeType[] = ["document", "faq", "manual", "policy", "note"];

export default function KnowledgeTypeSelect({ value, onChange, disabled }: Props) {
  return (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value as KnowledgeType)}
      disabled={disabled}
      className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 disabled:bg-gray-100 disabled:text-gray-500"
    >
      {types.map((t) => (
        <option key={t} value={t}>
          {t}
        </option>
      ))}
    </select>
  );
}