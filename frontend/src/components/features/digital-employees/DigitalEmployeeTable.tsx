"use client";

import Link from "next/link";
import StatusBadge from "@/components/ui/StatusBadge";
import type { AIEmployee } from "@/types/digital-employee";

interface DigitalEmployeeTableProps {
  employees: AIEmployee[];
  onDeleteClick: (employee: AIEmployee) => void;
}

export default function DigitalEmployeeTable({
  employees,
  onDeleteClick,
}: DigitalEmployeeTableProps) {
  return (
    <div className="overflow-x-auto rounded-lg border border-gray-200 bg-white">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-500">
              Name
            </th>
            <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-500">
              Provider
            </th>
            <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-500">
              Model
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
          {employees.map((emp) => (
            <tr key={emp.id} className="hover:bg-gray-50">
              <td className="px-4 py-3 text-sm font-medium text-gray-900">
                {emp.name}
              </td>
              <td className="px-4 py-3 text-sm text-gray-600">{emp.provider}</td>
              <td className="px-4 py-3 text-sm text-gray-600">{emp.model}</td>
              <td className="px-4 py-3 text-sm">
                <StatusBadge status={emp.status} />
              </td>
              <td className="px-4 py-3 text-sm text-gray-600">
                {new Date(emp.updated_at).toLocaleDateString()}
              </td>
              <td className="px-4 py-3 text-right text-sm">
                <Link
                  href={`/digital-employees/${emp.id}`}
                  className="text-blue-600 hover:text-blue-900 mr-3"
                >
                  View
                </Link>
                <Link
                  href={`/digital-employees/${emp.id}/edit`}
                  className="text-blue-600 hover:text-blue-900 mr-3"
                >
                  Edit
                </Link>
                <button
                  onClick={() => onDeleteClick(emp)}
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