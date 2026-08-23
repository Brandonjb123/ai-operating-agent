"use client";

import Link from "next/link";
import StatusBadge from "@/components/ui/StatusBadge";
import type { Knowledge } from "@/types/knowledge";

interface Props {
  items: Knowledge[];
  onDeleteClick: (item: Knowledge) => void;
}

export default function KnowledgeTable({ items, onDeleteClick }: Props) {
  return (
    <div className="overflow-x-auto rounded-lg border border-gray-200 bg-white">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-500">
              Title
            </th>
            <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-500">
              Source
            </th>
            <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-500">
              Type
            </th>
            <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-500">
              Status
            </th>
            <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-500">
              Updated At
            </th>
            <th className="px-4 py-3 text-right text-xs font-semibold uppercase tracking-wider text-gray-500">
              Actions
            </th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {items.map((item) => (
            <tr key={item.id} className="hover:bg-gray-50">
              <td className="px-4 py-3 text-sm font-medium text-gray-900">
                {item.title}
              </td>
              <td className="px-4 py-3 text-sm text-gray-600">{item.source}</td>
              <td className="px-4 py-3 text-sm text-gray-600">
                {item.knowledge_type}
              </td>
              <td className="px-4 py-3 text-sm">
                <StatusBadge status={item.status} />
              </td>
              <td className="px-4 py-3 text-sm text-gray-600">
                {new Date(item.updated_at).toLocaleDateString()}
              </td>
              <td className="px-4 py-3 text-right text-sm">
                <Link
                  href={`/knowledge/${item.id}`}
                  className="mr-3 text-blue-600 hover:text-blue-900"
                >
                  View
                </Link>
                <Link
                  href={`/knowledge/${item.id}/edit`}
                  className="mr-3 text-blue-600 hover:text-blue-900"
                >
                  Edit
                </Link>
                <button
                  onClick={() => onDeleteClick(item)}
                  className="text-red-600 hover:text-red-900"
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}