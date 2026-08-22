import ContentContainer from "@/components/layout/ContentContainer";
import PageHeader from "@/components/layout/PageHeader";

export default function OrganizationSettingsPage() {
  return (
    <ContentContainer>
      <PageHeader
        title="Organization"
        description="Pengaturan organisasi."
      />
      <div className="rounded-lg border border-dashed border-gray-300 bg-white p-12 text-center text-gray-500">
        Organization settings akan hadir nanti.
      </div>
    </ContentContainer>
  );
}