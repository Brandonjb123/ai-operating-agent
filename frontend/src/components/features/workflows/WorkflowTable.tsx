"use client";

import Link from "next/link";
import StatusBadge from "@/components/ui/StatusBadge";
import type { Workflow } from "@/types/workflow";

interface WorkflowTableProps {
  workflows: Workflow[];
  onDeleteClick: (workflow: Workflow) => void;
}

export default function WorkflowTable({
  workflows,
  onDeleteClick,
}: WorkflowTableProps) {
  return (
    <div className="overflow-x-auto rounded-lg border border-gray-200 bg-white">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-500">
              Name
            </th>
            <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-500">
              Status
            </th>
            <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-500">
              Trigger
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
          {workflows.map((workflow) => (
            <tr key={workflow.id} className="hover:bg-gray-50">
              <td className="px-4 py-3 text-sm font-medium text-gray-900">
                {workflow.name}
              </td>
              <td className="px-4 py-3 text-sm">
                <StatusBadge status={workflow.status} />
              </td>
              <td className="px-4 py-3 text-sm text-gray-600">
                {workflow.trigger_type}
              </td>
              <td className="px-4 py-3 text-sm text-gray-600">
                {new Date(workflow.updated_at).toLocaleDateString()}
              </td>
              <td className="px-4 py-3 text-right text-sm">
                <Link
                  href={`/workflows/${workflow.id}`}
                  className="mr-3 text-blue-600 hover:text-blue-900"
                >
                  View
                </Link>
                <Link
                  href={`/workflows/${workflow.id}/edit`}
                  className="mr-3 text-blue-600 hover:text-blue-900"
                >
                  Edit
                </Link>
                <button
                  onClick={() => onDeleteClick(workflow)}
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