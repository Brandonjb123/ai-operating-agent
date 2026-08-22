import ContentContainer from "@/components/layout/ContentContainer";
import PageHeader from "@/components/layout/PageHeader";

export default function WorkflowsPage() {
  return (
    <ContentContainer>
      <PageHeader
        title="Workflows"
        description="Otomasi proses dengan workflow."
      />
      <div className="rounded-lg border border-dashed border-gray-300 bg-white p-12 text-center text-gray-500">
        Workflow management UI akan diimplementasikan pada phase berikutnya.
      </div>
    </ContentContainer>
  );
}