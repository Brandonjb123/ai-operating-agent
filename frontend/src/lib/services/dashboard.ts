import { apiClient } from "@/lib/api";
import type { DashboardSummary } from "@/types/dashboard";

export async function getDashboardSummary(
  organizationId: string
): Promise<DashboardSummary> {
  return apiClient<DashboardSummary>(
    `/dashboard/summary?organization_id=${organizationId}`
  );
}