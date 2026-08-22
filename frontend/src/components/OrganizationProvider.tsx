"use client";

import React, { createContext, useContext, useEffect, useState } from "react";
import { useAuth } from "@/components/AuthProvider";
import { apiClient } from "@/lib/api";
import { getErrorMessage } from "@/lib/error";

interface Membership {
  id: string;
  organization_id: string;
  user_id: string;
  role_id: string;
  created_at: string;
  updated_at: string;
}

interface OrganizationState {
  currentOrganizationId: string | null;
  loading: boolean;
  error: string | null;
}

const OrganizationContext = createContext<OrganizationState | undefined>(undefined);

export function OrganizationProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const { user } = useAuth();
  const [state, setState] = useState<OrganizationState>({
    currentOrganizationId: null,
    loading: true,
    error: null,
  });

  useEffect(() => {
    let cancelled = false;

    async function loadOrganization() {
      if (!user) {
        if (!cancelled) {
          setState({ currentOrganizationId: null, loading: false, error: null });
        }
        return;
      }

      setState((prev) => ({ ...prev, loading: true }));

      try {
        const memberships = await apiClient<Membership[]>(
          `/memberships/?user_id=${user.id}`
        );

        if (cancelled) return;

        if (memberships.length > 0) {
          const orgId = memberships[0].organization_id;
          localStorage.setItem("aoa_current_organization_id", orgId);
          setState({ currentOrganizationId: orgId, loading: false, error: null });
        } else {
          const stored = localStorage.getItem("aoa_current_organization_id");
          setState({
            currentOrganizationId: stored || null,
            loading: false,
            error: null,
          });
        }
      } catch (err) {
        if (cancelled) return;
        const stored = localStorage.getItem("aoa_current_organization_id");
        setState({
          currentOrganizationId: stored || null,
          loading: false,
          error: getErrorMessage(err, "Failed to load organization"),
        });
      }
    }

    loadOrganization();

    return () => {
      cancelled = true;
    };
  }, [user]);

  return (
    <OrganizationContext.Provider value={state}>
      {children}
    </OrganizationContext.Provider>
  );
}

export function useOrganization() {
  const context = useContext(OrganizationContext);
  if (context === undefined) {
    throw new Error("useOrganization must be used within OrganizationProvider");
  }
  return context;
}