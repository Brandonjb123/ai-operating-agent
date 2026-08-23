"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import ContentContainer from "@/components/layout/ContentContainer";
import PageHeader from "@/components/layout/PageHeader";
import LoadingState from "@/components/ui/LoadingState";
import ErrorState from "@/components/ui/ErrorState";
import KnowledgeForm from "@/components/features/knowledge/KnowledgeForm";
import { useOrganization } from "@/components/OrganizationProvider";
import { useDigitalEmployees } from "@/hooks/useDigitalEmployees";
import { getKnowledge, updateKnowledge } from "@/lib/services/knowledge";
import { getErrorMessage } from "@/lib/error";
import type { Knowledge } from "@/types/knowledge";
import type { KnowledgeFormValues } from "@/components/features/knowledge/KnowledgeForm";

export default function EditKnowledgePage() {
  const params = useParams();
  const id = params.id as string;
  const router = useRouter();
  const { currentOrganizationId } = useOrganization();
  const { data: employees } = useDigitalEmployees(currentOrganizationId);

  const [item, setItem] = useState<Knowledge | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        const data = await getKnowledge(id);
        setItem(data);
      } catch (err) {
        setError(getErrorMessage(err, "Failed to load knowledge"));
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [id]);

  async function handleSubmit(values: KnowledgeFormValues) {
    const payload = {
      title: values.title,
      content: values.content,
      source: values.source,
      knowledge_type: values.knowledge_type,
      status: values.status,
      metadata: values.metadata,
    };
    await updateKnowledge(id, payload);
    router.push(`/knowledge/${id}`);
  }

  if (loading) return <LoadingState label="Loading knowledge..." />;
  if (error)
    return <ErrorState message={error} onRetry={() => window.location.reload()} />;
  if (!item) return null;

  const initialValues: KnowledgeFormValues = {
    ai_employee_id: item.ai_employee_id,
    title: item.title,
    content: item.content,
    source: item.source,
    knowledge_type: item.knowledge_type,
    status: item.status,
    metadata: item.metadata,
  };

  return (
    <ContentContainer>
      <PageHeader
        title="Edit Knowledge"
        description={`Update informasi untuk ${item.title}`}
      />
      <div className="rounded-lg border border-gray-200 bg-white p-6">
        <KnowledgeForm
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