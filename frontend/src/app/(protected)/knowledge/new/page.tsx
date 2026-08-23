"use client";

import { useRouter } from "next/navigation";
import ContentContainer from "@/components/layout/ContentContainer";
import PageHeader from "@/components/layout/PageHeader";
import KnowledgeForm from "@/components/features/knowledge/KnowledgeForm";
import { useOrganization } from "@/components/OrganizationProvider";
import { useDigitalEmployees } from "@/hooks/useDigitalEmployees";
import { createKnowledge } from "@/lib/services/knowledge";
import type { KnowledgeFormValues } from "@/components/features/knowledge/KnowledgeForm";
import type { CreateKnowledgeRequest } from "@/types/knowledge";

export default function NewKnowledgePage() {
  const router = useRouter();
  const { currentOrganizationId } = useOrganization();
  const { data: employees } = useDigitalEmployees(currentOrganizationId);

  async function handleSubmit(values: KnowledgeFormValues) {
    const payload: CreateKnowledgeRequest = {
      ai_employee_id: values.ai_employee_id,
      title: values.title,
      content: values.content,
      source: values.source,
      knowledge_type: values.knowledge_type,
      status: values.status,
      metadata: values.metadata,
    };
    const item = await createKnowledge(payload);
    router.push(`/knowledge/${item.id}`);
  }

  return (
    <ContentContainer>
      <PageHeader
        title="Create Knowledge"
        description="Tambahkan pengetahuan baru ke Digital Employee Anda."
      />
      <div className="rounded-lg border border-gray-200 bg-white p-6">
        <KnowledgeForm
          employees={employees}
          onSubmit={handleSubmit}
          submitLabel="Create Knowledge"
        />
      </div>
    </ContentContainer>
  );
}