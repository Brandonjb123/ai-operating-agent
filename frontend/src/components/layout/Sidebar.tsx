"use client";

import SidebarNav from "./SidebarNav";

export default function Sidebar({
  isOpen,
  onClose,
}: {
  isOpen: boolean;
  onClose: () => void;
}) {
  return (
    <>
      {/* Mobile drawer */}
      {isOpen && (
        <div className="fixed inset-0 z-50 lg:hidden">
          <div
            className="fixed inset-0 bg-gray-900/50"
            onClick={onClose}
          />
          <div className="fixed left-0 top-0 h-full w-64 bg-white shadow-xl">
            <div className="flex h-16 items-center justify-between border-b border-gray-200 px-4">
              <span className="text-lg font-bold text-gray-900">AOA</span>
              <button
                onClick={onClose}
                className="rounded-md p-2 text-gray-500 hover:bg-gray-100"
                aria-label="Close menu"
              >
                ✕
              </button>
            </div>
            <SidebarNav />
          </div>
        </div>
      )}

      {/* Desktop sidebar fixed */}
      <aside className="fixed inset-y-0 left-0 z-30 hidden w-64 flex-col border-r border-gray-200 bg-white lg:flex">
        <div className="flex h-16 items-center border-b border-gray-200 px-4">
          <span className="text-lg font-bold text-gray-900">AOA</span>
        </div>
        <SidebarNav />
      </aside>
    </>
  );
}