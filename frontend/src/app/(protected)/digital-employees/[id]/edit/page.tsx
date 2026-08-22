"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import ContentContainer from "@/components/layout/ContentContainer";
import PageHeader from "@/components/layout/PageHeader";
import LoadingState from "@/components/ui/LoadingState";
import ErrorState from "@/components/ui/ErrorState";
import DigitalEmployeeForm from "@/components/features/digital-employees/DigitalEmployeeForm";
import { getDigitalEmployee, updateDigitalEmployee } from "@/lib/services/digital-employees";
import { getErrorMessage } from "@/lib/error";
import type { AIEmployee, UpdateDigitalEmployeeRequest } from "@/types/digital-employee";

export default function EditDigitalEmployeePage() {
  const params = useParams();
  const id = params.id as string;
  const router = useRouter();
  const [employee, setEmployee] = useState<AIEmployee | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

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

  async function handleSubmit(payload: UpdateDigitalEmployeeRequest) {
    await updateDigitalEmployee(id, payload);
    router.push(`/digital-employees/${id}`);
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
        title="Edit Digital Employee"
        description={`Update informasi untuk ${employee.name}`}
      />
      <div className="rounded-lg border border-gray-200 bg-white p-6">
        <DigitalEmployeeForm
          initialValues={employee}
          onSubmit={handleSubmit}
          submitLabel="Save Changes"
        />
      </div>
    </ContentContainer>
  );
}