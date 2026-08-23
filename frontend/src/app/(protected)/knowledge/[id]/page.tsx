"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import ContentContainer from "@/components/layout/ContentContainer";
import PageHeader from "@/components/layout/PageHeader";
import LoadingState from "@/components/ui/LoadingState";
import ErrorState from "@/components/ui/ErrorState";
import StatusBadge from "@/components/ui/StatusBadge";
import DeleteConfirmDialog from "@/components/features/knowledge/DeleteConfirmDialog";
import { getKnowledge, deleteKnowledge } from "@/lib/services/knowledge";
import { getErrorMessage } from "@/lib/error";
import type { Knowledge } from "@/types/knowledge";

export default function KnowledgeDetailPage() {
  const params = useParams();
  const id = params.id as string;
  const router = useRouter();
  const [item, setItem] = useState<Knowledge | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showDelete, setShowDelete] = useState(false);
  const [deleteLoading, setDeleteLoading] = useState(false);

  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        const data = await getKnowledge(id);
        setItem(data);
      } catch (err) {
        setError(getErrorMessage(err, "Failed to load knowledge"));
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [id]);

  async function handleDelete() {
    setDeleteLoading(true);
    try {
      await deleteKnowledge(id);
      router.push("/knowledge");
    } catch (err) {
      alert(getErrorMessage(err, "Delete failed"));
      setShowDelete(false);
    } finally {
      setDeleteLoading(false);
    }
  }

  if (loading) return <LoadingState label="Loading knowledge..." />;
  if (error)
    return <ErrorState message={error} onRetry={() => window.location.reload()} />;
  if (!item) return null;

  return (
    <ContentContainer>
      <PageHeader
        title={item.title}
        description={`Source: ${item.source}`}
        action={
          <div className="flex gap-3">
            <Link
              href={`/knowledge/${id}/edit`}
              className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
            >
              Edit
            </Link>
            <button
              onClick={() => setShowDelete(true)}
              className="rounded-md bg-red-600 px-4 py-2 text-sm font-medium text-white hover:bg-red-700"
            >
              Delete
            </button>
          </div>
        }
      />

      <div className="space-y-6">
        <div className="rounded-lg border border-gray-200 bg-white p-6">
          <div className="flex items-center gap-4">
            <StatusBadge status={item.status} />
            <span className="text-sm text-gray-500">
              Type: {item.knowledge_type}
            </span>
          </div>
        </div>

        <div className="rounded-lg border border-gray-200 bg-white p-6">
          <h2 className="text-lg font-semibold text-gray-900">Content</h2>
          <p className="mt-2 whitespace-pre-wrap text-sm text-gray-800">
            {item.content}
          </p>
        </div>

        {item.metadata && (
          <div className="rounded-lg border border-gray-200 bg-white p-6">
            <h2 className="text-lg font-semibold text-gray-900">Metadata</h2>
            <pre className="mt-2 overflow-auto rounded bg-gray-50 p-4 text-sm text-gray-800">
              {JSON.stringify(item.metadata, null, 2)}
            </pre>
          </div>
        )}
      </div>

      <DeleteConfirmDialog
        knowledgeTitle={item.title}
        isOpen={showDelete}
        onCancel={() => setShowDelete(false)}
        onConfirm={handleDelete}
        loading={deleteLoading}
      />
    </ContentContainer>
  );
}