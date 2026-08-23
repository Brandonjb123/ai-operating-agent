"use client";

import { useState } from "react";
import Link from "next/link";
import ContentContainer from "@/components/layout/ContentContainer";
import PageHeader from "@/components/layout/PageHeader";
import LoadingState from "@/components/ui/LoadingState";
import ErrorState from "@/components/ui/ErrorState";
import WorkflowTable from "@/components/features/workflows/WorkflowTable";
import DeleteConfirmDialog from "@/components/features/workflows/DeleteConfirmDialog";
import { useOrganization } from "@/components/OrganizationProvider";
import { useDigitalEmployees } from "@/hooks/useDigitalEmployees";
import { useWorkflows } from "@/hooks/useWorkflows";
import { deleteWorkflow } from "@/lib/services/workflows";
import { getErrorMessage } from "@/lib/error";
import type { Workflow } from "@/types/workflow";

export default function WorkflowsPage() {
  const { currentOrganizationId, loading: orgLoading } = useOrganization();
  const {
    data: employees,
    loading: employeesLoading,
    error: employeesError,
  } = useDigitalEmployees(currentOrganizationId);

  const [selectedEmployeeId, setSelectedEmployeeId] = useState<string | null>(null);

  // Derived state: jika user belum memilih, gunakan employee pertama sebagai default.
  // Ini menghindari setState di dalam useEffect.
  const effectiveEmployeeId =
    selectedEmployeeId || (employees.length > 0 ? employees[0].id : null);

  const {
    data: workflows,
    loading: workflowsLoading,
    error: workflowsError,
    refetch,
  } = useWorkflows(effectiveEmployeeId);

  const [deleteTarget, setDeleteTarget] = useState<Workflow | null>(null);
  const [deleteLoading, setDeleteLoading] = useState(false);

  async function handleDelete() {
    if (!deleteTarget) return;
    setDeleteLoading(true);
    try {
      await deleteWorkflow(deleteTarget.id);
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
        title="Workflows"
        description="Kelola workflow digital employee Anda."
        action={
          <Link
            href="/workflows/new"
            className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
          >
            New Workflow
          </Link>
        }
      />

      {employees.length === 0 ? (
        <div className="rounded-lg border border-dashed border-gray-300 bg-white p-12 text-center">
          <p className="text-gray-600">
            Anda belum memiliki Digital Employee.
          </p>
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

          {workflowsLoading && <LoadingState label="Loading workflows..." />}
          {workflowsError && (
            <ErrorState message={workflowsError} onRetry={refetch} />
          )}
          {!workflowsLoading &&
            !workflowsError &&
            workflows.length === 0 && (
              <div className="rounded-lg border border-dashed border-gray-300 bg-white p-12 text-center">
                <p className="text-gray-600">No workflows yet</p>
                <Link
                  href="/workflows/new"
                  className="mt-4 inline-block rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
                >
                  Create Workflow
                </Link>
              </div>
            )}
          {!workflowsLoading && !workflowsError && workflows.length > 0 && (
            <WorkflowTable
              workflows={workflows}
              onDeleteClick={setDeleteTarget}
            />
          )}
        </>
      )}

      <DeleteConfirmDialog
        workflowName={deleteTarget?.name || ""}
        isOpen={!!deleteTarget}
        onCancel={() => setDeleteTarget(null)}
        onConfirm={handleDelete}
        loading={deleteLoading}
      />
    </ContentContainer>
  );
}