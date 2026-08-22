import ContentContainer from "@/components/layout/ContentContainer";
import PageHeader from "@/components/layout/PageHeader";

export default function RolesPage() {
  return (
    <ContentContainer>
      <PageHeader
        title="Roles & Permissions"
        description="Kelola peran dan izin pengguna."
      />
      <div className="rounded-lg border border-dashed border-gray-300 bg-white p-12 text-center text-gray-500">
        Role management akan hadir nanti.
      </div>
    </ContentContainer>
  );
}