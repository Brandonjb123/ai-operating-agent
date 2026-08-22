import ContentContainer from "@/components/layout/ContentContainer";
import PageHeader from "@/components/layout/PageHeader";

export default function KnowledgePage() {
  return (
    <ContentContainer>
      <PageHeader
        title="Knowledge"
        description="Kelola basis pengetahuan digital employee."
      />
      <div className="rounded-lg border border-dashed border-gray-300 bg-white p-12 text-center text-gray-500">
        Knowledge management UI akan hadir nanti.
      </div>
    </ContentContainer>
  );
}