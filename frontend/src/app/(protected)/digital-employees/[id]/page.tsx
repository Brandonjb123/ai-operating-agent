"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import ContentContainer from "@/components/layout/ContentContainer";
import PageHeader from "@/components/layout/PageHeader";
import LoadingState from "@/components/ui/LoadingState";
import ErrorState from "@/components/ui/ErrorState";
import StatusBadge from "@/components/ui/StatusBadge";
import DeleteConfirmDialog from "@/components/features/digital-employees/DeleteConfirmDialog";
import { getDigitalEmployee, deleteDigitalEmployee } from "@/lib/services/digital-employees";
import { getErrorMessage } from "@/lib/error";
import type { AIEmployee } from "@/types/digital-employee";

export default function DigitalEmployeeDetailPage() {
  const params = useParams();
  const id = params.id as string;
  const router = useRouter();
  const [employee, setEmployee] = useState<AIEmployee | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showDelete, setShowDelete] = useState(false);
  const [deleteLoading, setDeleteLoading] = useState(false);

  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        const data = await getDigitalEmployee(id);
        setEmployee(data);
      } catch (err) {
        setError(getErrorMessage(err, "Failed to load digital employee"));
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [id]);

  async function handleDelete() {
    setDeleteLoading(true);
    try {
      await deleteDigitalEmployee(id);
      router.push("/digital-employees");
    } catch (err) {
      alert(getErrorMessage(err, "Delete failed"));
      setShowDelete(false);
    } finally {
      setDeleteLoading(false);
    }
  }

  if (loading) return <LoadingState label="Loading digital employee..." />;
  if (error)
    return (
      <ErrorState message={error} onRetry={() => window.location.reload()} />
    );
  if (!employee) return null;

  return (
    <ContentContainer>
      <PageHeader
        title={employee.name}
        description={employee.description || ""}
        action={
          <div className="flex gap-3">
            <Link
              href={`/digital-employees/${id}/edit`}
              className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
            >
              Edit
            </Link>
            <button
              onClick={() => setShowDelete(true)}
              className="rounded-md bg-red-600 px-4 py-2 text-sm font-medium text-white hover:bg-red-700"
            >
              Delete
            </button>
          </div>
        }
      />
      <div className="rounded-lg border border-gray-200 bg-white p-6">
        <div className="flex items-center gap-4">
          <StatusBadge status={employee.status} />
          <span className="text-sm text-gray-500">
            Provider: {employee.provider}
          </span>
          <span className="text-sm text-gray-500">Model: {employee.model}</span>
        </div>
        <dl className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div>
            <dt className="text-sm font-medium text-gray-500">Temperature</dt>
            <dd className="mt-1 text-sm text-gray-900">{employee.temperature}</dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">Max Tokens</dt>
            <dd className="mt-1 text-sm text-gray-900">{employee.max_tokens}</dd>
          </div>
          <div className="sm:col-span-2">
            <dt className="text-sm font-medium text-gray-500">System Prompt</dt>
            <dd className="mt-1 text-sm text-gray-900 whitespace-pre-wrap">
              {employee.system_prompt}
            </dd>
          </div>
        </dl>
      </div>
      <div className="mt-6">
        <nav className="flex space-x-4 border-b border-gray-200">
          <button className="border-b-2 border-blue-600 px-4 py-2 text-sm font-medium text-blue-600">
            Overview
          </button>
          <button className="px-4 py-2 text-sm font-medium text-gray-500 cursor-not-allowed">
            Memory
          </button>
          <button className="px-4 py-2 text-sm font-medium text-gray-500 cursor-not-allowed">
            Knowledge
          </button>
          <button className="px-4 py-2 text-sm font-medium text-gray-500 cursor-not-allowed">
            Workflows
          </button>
        </nav>
      </div>
      <DeleteConfirmDialog
        employeeName={employee.name}
        isOpen={showDelete}
        onCancel={() => setShowDelete(false)}
        onConfirm={handleDelete}
        loading={deleteLoading}
      />
    </ContentContainer>
  );
}