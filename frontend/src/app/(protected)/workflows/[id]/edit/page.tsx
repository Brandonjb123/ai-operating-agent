"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import ContentContainer from "@/components/layout/ContentContainer";
import PageHeader from "@/components/layout/PageHeader";
import LoadingState from "@/components/ui/LoadingState";
import ErrorState from "@/components/ui/ErrorState";
import WorkflowForm from "@/components/features/workflows/WorkflowForm";
import { useOrganization } from "@/components/OrganizationProvider";
import { useDigitalEmployees } from "@/hooks/useDigitalEmployees";
import { getWorkflow, updateWorkflow } from "@/lib/services/workflows";
import { getErrorMessage } from "@/lib/error";
import type { Workflow } from "@/types/workflow";
import type { WorkflowFormValues } from "@/components/features/workflows/WorkflowForm";

export default function EditWorkflowPage() {
  const params = useParams();
  const id = params.id as string;
  const router = useRouter();
  const { currentOrganizationId } = useOrganization();
  const { data: employees } = useDigitalEmployees(currentOrganizationId);

  const [workflow, setWorkflow] = useState<Workflow | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        const data = await getWorkflow(id);
        setWorkflow(data);
      } catch (err) {
        setError(getErrorMessage(err, "Failed to load workflow"));
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [id]);

  async function handleSubmit(values: WorkflowFormValues) {
    const payload = {
      name: values.name,
      description: values.description,
      definition: { steps: values.steps },
      trigger_type: values.trigger_type,
      status: values.status,
    };
    await updateWorkflow(id, payload);
    router.push(`/workflows/${id}`);
  }

  if (loading) return <LoadingState label="Loading workflow..." />;
  if (error)
    return <ErrorState message={error} onRetry={() => window.location.reload()} />;
  if (!workflow) return null;

  const initialValues: WorkflowFormValues = {
    ai_employee_id: workflow.ai_employee_id,
    name: workflow.name,
    description: workflow.description || "",
    trigger_type: workflow.trigger_type,
    status: workflow.status,
    steps: workflow.definition.steps,
  };

  return (
    <ContentContainer>
      <PageHeader
        title="Edit Workflow"
        description={`Update informasi untuk ${workflow.name}`}
      />
      <div className="rounded-lg border border-gray-200 bg-white p-6">
        <WorkflowForm
          employees={employees}
          initialValues={initialValues}
          onSubmit={handleSubmit}
          submitLabel="Save Changes"
          disableEmployeeSelect
        />
      </div>
    </ContentContainer>
  );
}