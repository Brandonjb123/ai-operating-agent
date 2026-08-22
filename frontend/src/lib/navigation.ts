export interface NavItem {
  label: string;
  href: string;
  icon?: string; // untuk V1 bisa diabaikan
}

export interface NavSection {
  title: string;
  items: NavItem[];
}

export const navigationSections: NavSection[] = [
  {
    title: "WORKSPACE",
    items: [
      { label: "Dashboard", href: "/dashboard" },
      { label: "Digital Employees", href: "/digital-employees" },
    ],
  },
  {
    title: "AUTOMATION",
    items: [
      { label: "Workflows", href: "/workflows" },
      { label: "Knowledge", href: "/knowledge" },
    ],
  },
  {
    title: "GOVERNANCE & SETTINGS",
    items: [
      { label: "Organization", href: "/settings/organization" },
      { label: "Roles & Permissions", href: "/settings/roles" },
      { label: "Memberships", href: "/settings/memberships" },
    ],
  },
];