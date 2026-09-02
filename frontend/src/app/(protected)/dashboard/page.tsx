"use client";

import ContentContainer from "@/components/layout/ContentContainer";
import PageHeader from "@/components/layout/PageHeader";
import LoadingState from "@/components/ui/LoadingState";
import ErrorState from "@/components/ui/ErrorState";
import DashboardMetricCard from "@/components/features/dashboard/DashboardMetricCard";
import { useOrganization } from "@/components/OrganizationProvider";
import { useDashboardSummary } from "@/hooks/useDashboardSummary";

export default function DashboardPage() {
  const { currentOrganizationId, loading: orgLoading } = useOrganization();
  const { data: summary, loading, error, refetch } =
    useDashboardSummary(currentOrganizationId);

  if (orgLoading) {
    return <LoadingState label="Loading organization..." />;
  }

  return (
    <ContentContainer>
      <PageHeader
        title="Dashboard"
        description="Ringkasan workforce digital Anda."
      />

      {loading && <LoadingState label="Loading dashboard summary..." />}
      {error && <ErrorState message={error} onRetry={refetch} />}
      {!loading && !error && summary && (
        <dl className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5">
          <DashboardMetricCard
            title="Total Digital Employees"
            value={summary.total_digital_employees}
          />
          <DashboardMetricCard
            title="Active Digital Employees"
            value={summary.active_digital_employees}
          />
          <DashboardMetricCard
            title="Total Knowledge"
            value={summary.total_knowledge}
          />
          <DashboardMetricCard
            title="Total Memory"
            value={summary.total_memory}
          />
          <DashboardMetricCard
            title="Total Workflows"
            value={summary.total_workflows}
          />
        </dl>
      )}
    </ContentContainer>
  );
}