"use client";

import { useState, useEffect, useCallback } from "react";
import { getDashboardSummary } from "@/lib/services/dashboard";
import type { DashboardSummary } from "@/types/dashboard";
import { getErrorMessage } from "@/lib/error";

export function useDashboardSummary(organizationId: string | null) {
  const [data, setData] = useState<DashboardSummary | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    if (!organizationId) {
      setData(null);
      setLoading(false);
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const summary = await getDashboardSummary(organizationId);
      setData(summary);
    } catch (err) {
      setError(getErrorMessage(err, "Failed to load dashboard summary"));
    } finally {
      setLoading(false);
    }
  }, [organizationId]);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
}