"use client";

import UserMenu from "./UserMenu";

export default function Header({ onMenuClick }: { onMenuClick: () => void }) {
  return (
    <header className="sticky top-0 z-20 flex h-16 items-center justify-between border-b border-gray-200 bg-white px-4 lg:px-6">
      <div className="flex items-center gap-3">
        <button
          onClick={onMenuClick}
          className="rounded-md p-2 text-gray-500 hover:bg-gray-100 lg:hidden"
          aria-label="Open menu"
        >
          ☰
        </button>
        <div className="text-sm font-medium text-gray-600">
          AOA / Digital Workforce
        </div>
      </div>
      <UserMenu />
    </header>
  );
}