interface DashboardMetricCardProps {
  title: string;
  value: number;
}

export default function DashboardMetricCard({
  title,
  value,
}: DashboardMetricCardProps) {
  return (
    <div className="rounded-lg border border-gray-200 bg-white p-6">
      <dt className="truncate text-sm font-medium text-gray-500">{title}</dt>
      <dd className="mt-2 text-3xl font-semibold text-gray-900">{value}</dd>
    </div>
  );
}