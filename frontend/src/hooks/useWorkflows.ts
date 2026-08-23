"use client";

import { useState, useEffect, useCallback } from "react";
import { listWorkflows } from "@/lib/services/workflows";
import type { Workflow } from "@/types/workflow";
import { getErrorMessage } from "@/lib/error";

export function useWorkflows(aiEmployeeId: string | null) {
  const [data, setData] = useState<Workflow[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    if (!aiEmployeeId) {
      setData([]);
      setLoading(false);
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await listWorkflows(aiEmployeeId);
      setData(result);
    } catch (err) {
      setError(getErrorMessage(err, "Failed to load workflows"));
    } finally {
      setLoading(false);
    }
  }, [aiEmployeeId]);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
}