import ContentContainer from "@/components/layout/ContentContainer";
import PageHeader from "@/components/layout/PageHeader";

export default function WorkflowDetailPage({
  params,
}: {
  params: { id: string };
}) {
  return (
    <ContentContainer>
      <PageHeader
        title="Workflow Detail"
        description={`Detail untuk ID: ${params.id}`}
      />
      <div className="rounded-lg border border-dashed border-gray-300 bg-white p-12 text-center text-gray-500">
        Detail workflow akan hadir nanti.
      </div>
    </ContentContainer>
  );
}