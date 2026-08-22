"use client";

import { Provider } from "@/types/digital-employee";

interface ProviderSelectProps {
  value: Provider;
  onChange: (value: Provider) => void;
  disabled?: boolean;
}

const providers: Provider[] = ["groq", "openai", "anthropic", "google", "ollama"];

export default function ProviderSelect({
  value,
  onChange,
  disabled,
}: ProviderSelectProps) {
  return (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value as Provider)}
      disabled={disabled}
      className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
    >
      {providers.map((p) => (
        <option key={p} value={p}>
          {p}
        </option>
      ))}
    </select>
  );
}