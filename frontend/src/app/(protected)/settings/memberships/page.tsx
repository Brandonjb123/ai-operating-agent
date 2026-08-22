import ContentContainer from "@/components/layout/ContentContainer";
import PageHeader from "@/components/layout/PageHeader";

export default function MembershipsPage() {
  return (
    <ContentContainer>
      <PageHeader
        title="Memberships"
        description="Kelola keanggotaan organisasi."
      />
      <div className="rounded-lg border border-dashed border-gray-300 bg-white p-12 text-center text-gray-500">
        Membership management akan hadir nanti.
      </div>
    </ContentContainer>
  );
}