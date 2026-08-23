"use client";

import { useRouter } from "next/navigation";
import ContentContainer from "@/components/layout/ContentContainer";
import PageHeader from "@/components/layout/PageHeader";
import WorkflowForm from "@/components/features/workflows/WorkflowForm";
import { useOrganization } from "@/components/OrganizationProvider";
import { useDigitalEmployees } from "@/hooks/useDigitalEmployees";
import { createWorkflow } from "@/lib/services/workflows";
import type { WorkflowFormValues } from "@/components/features/workflows/WorkflowForm"; // or define inline

export default function NewWorkflowPage() {
  const router = useRouter();
  const { currentOrganizationId } = useOrganization();
  const { data: employees } = useDigitalEmployees(currentOrganizationId);

  async function handleSubmit(values: WorkflowFormValues) {
    const payload = {
      ai_employee_id: values.ai_employee_id,
      name: values.name,
      description: values.description,
      definition: { steps: values.steps },
      trigger_type: values.trigger_type,
      status: values.status,
    };
    const workflow = await createWorkflow(payload);
    router.push(`/workflows/${workflow.id}`);
  }

  return (
    <ContentContainer>
      <PageHeader
        title="Create Workflow"
        description="Buat workflow baru untuk Digital Employee Anda."
      />
      <div className="rounded-lg border border-gray-200 bg-white p-6">
        <WorkflowForm
          employees={employees}
          onSubmit={handleSubmit}
          submitLabel="Create Workflow"
        />
      </div>
    </ContentContainer>
  );
}