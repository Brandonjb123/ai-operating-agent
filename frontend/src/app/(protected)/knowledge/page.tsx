"use client";

import { useState } from "react";
import Link from "next/link";
import ContentContainer from "@/components/layout/ContentContainer";
import PageHeader from "@/components/layout/PageHeader";
import LoadingState from "@/components/ui/LoadingState";
import ErrorState from "@/components/ui/ErrorState";
import KnowledgeTable from "@/components/features/knowledge/KnowledgeTable";
import DeleteConfirmDialog from "@/components/features/knowledge/DeleteConfirmDialog";
import { useOrganization } from "@/components/OrganizationProvider";
import { useDigitalEmployees } from "@/hooks/useDigitalEmployees";
import { useKnowledge } from "@/hooks/useKnowledge";
import { deleteKnowledge } from "@/lib/services/knowledge";
import { getErrorMessage } from "@/lib/error";
import type { Knowledge } from "@/types/knowledge";

export default function KnowledgePage() {
  const { currentOrganizationId, loading: orgLoading } = useOrganization();
  const {
    data: employees,
    loading: employeesLoading,
    error: employeesError,
  } = useDigitalEmployees(currentOrganizationId);

  const [selectedEmployeeId, setSelectedEmployeeId] = useState<string | null>(null);
  const effectiveEmployeeId =
    selectedEmployeeId || (employees.length > 0 ? employees[0].id : null);

  const {
    data: knowledgeItems,
    loading: knowledgeLoading,
    error: knowledgeError,
    refetch,
  } = useKnowledge(effectiveEmployeeId);

  const [deleteTarget, setDeleteTarget] = useState<Knowledge | null>(null);
  const [deleteLoading, setDeleteLoading] = useState(false);

  async function handleDelete() {
    if (!deleteTarget) return;
    setDeleteLoading(true);
    try {
      await deleteKnowledge(deleteTarget.id);
      setDeleteTarget(null);
      refetch();
    } catch (err) {
      alert(getErrorMessage(err, "Delete failed"));
    } finally {
      setDeleteLoading(false);
    }
  }

  if (orgLoading || employeesLoading) {
    return <LoadingState label="Loading..." />;
  }

  if (employeesError) {
    return <ErrorState message={employeesError} />;
  }

  return (
    <ContentContainer>
      <PageHeader
        title="Knowledge"
        description="Kelola basis pengetahuan digital employee Anda."
        action={
          <Link
            href="/knowledge/new"
            className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
          >
            New Knowledge
          </Link>
        }
      />

      {employees.length === 0 ? (
        <div className="rounded-lg border border-dashed border-gray-300 bg-white p-12 text-center">
          <p className="text-gray-600">Anda belum memiliki Digital Employee.</p>
          <Link
            href="/digital-employees/new"
            className="mt-4 inline-block rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
          >
            Create Digital Employee
          </Link>
        </div>
      ) : (
        <>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700">
              Digital Employee
            </label>
            <select
              value={effectiveEmployeeId || ""}
              onChange={(e) => setSelectedEmployeeId(e.target.value)}
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 sm:w-72"
            >
              {employees.map((emp) => (
                <option key={emp.id} value={emp.id}>
                  {emp.name}
                </option>
              ))}
            </select>
          </div>

          {knowledgeLoading && <LoadingState label="Loading knowledge..." />}
          {knowledgeError && (
            <ErrorState message={knowledgeError} onRetry={refetch} />
          )}
          {!knowledgeLoading && !knowledgeError && knowledgeItems.length === 0 && (
            <div className="rounded-lg border border-dashed border-gray-300 bg-white p-12 text-center">
              <p className="text-gray-600">No knowledge items yet</p>
              <Link
                href="/knowledge/new"
                className="mt-4 inline-block rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
              >
                Create Knowledge
              </Link>
            </div>
          )}
          {!knowledgeLoading && !knowledgeError && knowledgeItems.length > 0 && (
            <KnowledgeTable
              items={knowledgeItems}
              onDeleteClick={setDeleteTarget}
            />
          )}
        </>
      )}

      <DeleteConfirmDialog
        knowledgeTitle={deleteTarget?.title || ""}
        isOpen={!!deleteTarget}
        onCancel={() => setDeleteTarget(null)}
        onConfirm={handleDelete}
        loading={deleteLoading}
      />
    </ContentContainer>
  );
}