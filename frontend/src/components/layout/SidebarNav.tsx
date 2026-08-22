"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { navigationSections } from "@/lib/navigation";

export default function SidebarNav() {
  const pathname = usePathname();

  return (
    <nav className="flex-1 space-y-6 overflow-y-auto px-3 py-4">
      {navigationSections.map((section) => (
        <div key={section.title}>
          <h2 className="mb-2 px-2 text-xs font-semibold uppercase tracking-wider text-gray-400">
            {section.title}
          </h2>
          <ul className="space-y-1">
            {section.items.map((item) => {
              const isActive =
                pathname === item.href ||
                (item.href !== "/dashboard" && pathname.startsWith(item.href));
              return (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    className={
                      isActive
                        ? "block rounded-md bg-blue-50 px-3 py-2 text-sm font-semibold text-blue-700"
                        : "block rounded-md px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100"
                    }
                  >
                    {item.label}
                  </Link>
                </li>
              );
            })}
          </ul>
        </div>
      ))}
    </nav>
  );
}