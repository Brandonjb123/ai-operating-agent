"use client";

import { useAuth } from "@/components/AuthProvider";

export default function UserMenu() {
  const { user, logout } = useAuth();

  if (!user) return null;

  return (
    <div className="flex items-center gap-3">
      <div className="text-right">
        <p className="text-sm font-semibold text-gray-900">{user.full_name}</p>
        <p className="text-xs text-gray-500">{user.email}</p>
      </div>
      <button
        onClick={logout}
        className="rounded-md bg-gray-900 px-3 py-1.5 text-sm font-medium text-white hover:bg-gray-700"
      >
        Logout
      </button>
    </div>
  );
}