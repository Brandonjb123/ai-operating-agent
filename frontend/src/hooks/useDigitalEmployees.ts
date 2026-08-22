"use client";

import { useState, useEffect, useCallback } from "react";
import { listDigitalEmployees } from "@/lib/services/digital-employees";
import type { AIEmployee } from "@/types/digital-employee";
import { getErrorMessage } from "@/lib/error";

export function useDigitalEmployees(organizationId: string | null) {
  const [data, setData] = useState<AIEmployee[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    if (!organizationId) {
      setData([]);
      setLoading(false);
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await listDigitalEmployees(organizationId);
      setData(result);
    } catch (err) {
      setError(getErrorMessage(err, "Failed to load digital employees"));
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