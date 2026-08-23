"use client";

import { useState, useEffect, useCallback } from "react";
import { listKnowledge } from "@/lib/services/knowledge";
import type { Knowledge } from "@/types/knowledge";
import { getErrorMessage } from "@/lib/error";

export function useKnowledge(aiEmployeeId: string | null) {
  const [data, setData] = useState<Knowledge[]>([]);
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
      const result = await listKnowledge(aiEmployeeId);
      setData(result);
    } catch (err) {
      setError(getErrorMessage(err, "Failed to load knowledge"));
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