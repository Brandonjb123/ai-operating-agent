"use client";

import { useRouter } from "next/navigation";
import ContentContainer from "@/components/layout/ContentContainer";
import PageHeader from "@/components/layout/PageHeader";
import DigitalEmployeeForm from "@/components/features/digital-employees/DigitalEmployeeForm";
import { useOrganization } from "@/components/OrganizationProvider";
import { createDigitalEmployee } from "@/lib/services/digital-employees";
import type {
  CreateDigitalEmployeeRequest,
  UpdateDigitalEmployeeRequest,
} from "@/types/digital-employee";


export default function NewDigitalEmployeePage() {
  const router = useRouter();
  const { currentOrganizationId } = useOrganization();

  async function handleSubmit(
  values: CreateDigitalEmployeeRequest | UpdateDigitalEmployeeRequest
) {
  if (!currentOrganizationId) throw new Error("No organization selected");
  const payload = {
    ...values,
    organization_id: currentOrganizationId,
  } as CreateDigitalEmployeeRequest;
  const employee = await createDigitalEmployee(payload);
  router.push(`/digital-employees/${employee.id}`);
}

  return (
    <ContentContainer>
      <PageHeader
        title="Create Digital Employee"
        description="Tambahkan digital employee baru ke organisasi Anda."
      />
      <div className="rounded-lg border border-gray-200 bg-white p-6">
        <DigitalEmployeeForm
          initialValues={{ organization_id: currentOrganizationId || "" }}
          onSubmit={handleSubmit}
          submitLabel="Create Digital Employee"
        />
      </div>
    </ContentContainer>
  );
}