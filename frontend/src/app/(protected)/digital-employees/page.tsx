"use client";

import { useState } from "react";
import Link from "next/link";
import ContentContainer from "@/components/layout/ContentContainer";
import PageHeader from "@/components/layout/PageHeader";
import LoadingState from "@/components/ui/LoadingState";
import ErrorState from "@/components/ui/ErrorState";
import DigitalEmployeeTable from "@/components/features/digital-employees/DigitalEmployeeTable";
import DeleteConfirmDialog from "@/components/features/digital-employees/DeleteConfirmDialog";
import { useOrganization } from "@/components/OrganizationProvider";
import { useDigitalEmployees } from "@/hooks/useDigitalEmployees";
import { deleteDigitalEmployee } from "@/lib/services/digital-employees";
import { getErrorMessage } from "@/lib/error";
import type { AIEmployee } from "@/types/digital-employee";

export default function DigitalEmployeesPage() {
  const { currentOrganizationId, loading: orgLoading } = useOrganization();
  const {
    data: employees,
    loading,
    error,
    refetch,
  } = useDigitalEmployees(currentOrganizationId);
  const [deleteTarget, setDeleteTarget] = useState<AIEmployee | null>(null);
  const [deleteLoading, setDeleteLoading] = useState(false);

  const handleDelete = async () => {
    if (!deleteTarget) return;
    setDeleteLoading(true);
    try {
      await deleteDigitalEmployee(deleteTarget.id);
      setDeleteTarget(null);
      refetch();
    } catch (err) {
      alert(getErrorMessage(err, "Delete failed"));
    } finally {
      setDeleteLoading(false);
    }
  };

  if (orgLoading) return <LoadingState label="Loading organization..." />;

  return (
    <ContentContainer>
      <PageHeader
        title="Digital Employees"
        description="Kelola digital workforce Anda."
        action={
          <Link
            href="/digital-employees/new"
            className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
          >
            New Digital Employee
          </Link>
        }
      />

      {loading && <LoadingState label="Loading digital employees..." />}
      {error && <ErrorState message={error} onRetry={refetch} />}
      {!loading && !error && employees.length === 0 && (
        <div className="rounded-lg border border-dashed border-gray-300 bg-white p-12 text-center">
          <p className="text-gray-600">No digital employees yet</p>
          <Link
            href="/digital-employees/new"
            className="mt-4 inline-block rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
          >
            Create Digital Employee
          </Link>
        </div>
      )}
      {!loading && !error && employees.length > 0 && (
        <DigitalEmployeeTable
          employees={employees}
          onDeleteClick={setDeleteTarget}
        />
      )}

      <DeleteConfirmDialog
        employeeName={deleteTarget?.name || ""}
        isOpen={!!deleteTarget}
        onCancel={() => setDeleteTarget(null)}
        onConfirm={handleDelete}
        loading={deleteLoading}
      />
    </ContentContainer>
  );
}