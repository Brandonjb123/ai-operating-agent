"use client";

import { AuthProvider } from "@/components/AuthProvider";
import { OrganizationProvider } from "@/components/OrganizationProvider";

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <AuthProvider>
      <OrganizationProvider>{children}</OrganizationProvider>
    </AuthProvider>
  );
}