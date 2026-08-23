"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import ContentContainer from "@/components/layout/ContentContainer";
import PageHeader from "@/components/layout/PageHeader";
import LoadingState from "@/components/ui/LoadingState";
import ErrorState from "@/components/ui/ErrorState";
import StatusBadge from "@/components/ui/StatusBadge";
import DeleteConfirmDialog from "@/components/features/workflows/DeleteConfirmDialog";
import { getWorkflow, deleteWorkflow } from "@/lib/services/workflows";
import { getErrorMessage } from "@/lib/error";
import type { Workflow } from "@/types/workflow";

export default function WorkflowDetailPage() {
  const params = useParams();
  const id = params.id as string;
  const router = useRouter();
  const [workflow, setWorkflow] = useState<Workflow | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showDelete, setShowDelete] = useState(false);
  const [deleteLoading, setDeleteLoading] = useState(false);

  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        const data = await getWorkflow(id);
        setWorkflow(data);
      } catch (err) {
        setError(getErrorMessage(err, "Failed to load workflow"));
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [id]);

  async function handleDelete() {
    setDeleteLoading(true);
    try {
      await deleteWorkflow(id);
      router.push("/workflows");
    } catch (err) {
      alert(getErrorMessage(err, "Delete failed"));
      setShowDelete(false);
    } finally {
      setDeleteLoading(false);
    }
  }

  if (loading) return <LoadingState label="Loading workflow..." />;
  if (error)
    return <ErrorState message={error} onRetry={() => window.location.reload()} />;
  if (!workflow) return null;

  return (
    <ContentContainer>
      <PageHeader
        title={workflow.name}
        description={workflow.description || ""}
        action={
          <div className="flex gap-3">
            <Link
              href={`/workflows/${id}/edit`}
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
            <StatusBadge status={workflow.status} />
            <span className="text-sm text-gray-500">
              Trigger: {workflow.trigger_type}
            </span>
          </div>
        </div>

        <div className="rounded-lg border border-gray-200 bg-white p-6">
          <h2 className="text-lg font-semibold text-gray-900">Steps</h2>
          {workflow.definition.steps.length === 0 ? (
            <p className="mt-2 text-sm text-gray-500">No steps defined.</p>
          ) : (
            <div className="mt-4 space-y-4">
              {workflow.definition.steps.map((step, index) => (
                <div
                  key={step.id}
                  className="rounded-md border border-gray-200 bg-gray-50 p-4"
                >
                  <p className="text-xs font-semibold uppercase text-gray-500">
                    Step {index + 1} — LLM
                  </p>
                  <p className="mt-2 whitespace-pre-wrap text-sm text-gray-800">
                    {step.config.prompt}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      <DeleteConfirmDialog
        workflowName={workflow.name}
        isOpen={showDelete}
        onCancel={() => setShowDelete(false)}
        onConfirm={handleDelete}
        loading={deleteLoading}
      />
    </ContentContainer>
  );
}