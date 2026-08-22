"use client";

import ContentContainer from "@/components/layout/ContentContainer";
import PageHeader from "@/components/layout/PageHeader";
import { useAuth } from "@/components/AuthProvider";

export default function DashboardPage() {
  const { user } = useAuth();

  return (
    <ContentContainer>
      <PageHeader
        title="Dashboard"
        description="Selamat datang di AOA Digital Workforce."
      />
      <div className="rounded-lg border border-dashed border-gray-300 bg-white p-8 text-center">
        <p className="text-gray-600">
          Dashboard analytics akan hadir di fase berikutnya.
        </p>
        <p className="mt-2 text-sm text-gray-500">
          Signed in as <span className="font-semibold">{user?.full_name}</span> ({user?.email})
        </p>
      </div>
    </ContentContainer>
  );
}