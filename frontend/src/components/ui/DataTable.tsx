import * as React from "react";
import { useTranslation } from "react-i18next";
import { cn } from "@/lib/utils";
import { EmptyState } from "./EmptyState";
import { Skeleton } from "./Skeleton";
import { Inbox } from "lucide-react";

export interface DataTableColumn<T> {
  key: string;
  header: string;
  render?: (row: T) => React.ReactNode;
  sortable?: boolean;
  width?: string;
}

export interface DataTableProps<T> {
  columns: DataTableColumn<T>[];
  data: T[];
  loading?: boolean;
  emptyMessage?: string;
  pagination?: {
    page: number;
    totalPages: number;
    onPageChange: (page: number) => void;
  };
  onRowClick?: (row: T) => void;
  rowClassName?: (row: T) => string;
}

export function DataTable<T extends Record<string, unknown>>({
  columns,
  data,
  loading = false,
  emptyMessage,
  pagination,
  onRowClick,
  rowClassName,
}: DataTableProps<T>) {
  const { t } = useTranslation();
  const resolvedEmptyMessage = emptyMessage ?? t("common.noData");

  if (loading) {
    return (
      <div className="w-full overflow-x-auto rounded-xl border border-stone-200/60 bg-white">
        <table className="w-full text-sm">
          <thead className="bg-stone-50 text-xs font-medium uppercase tracking-wider text-stone-500">
            <tr>
              {columns.map((col) => (
                <th key={col.key} className="px-5 py-3 text-left" style={{ width: col.width }}>
                  {col.header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {[1, 2, 3, 4, 5].map((i) => (
              <tr key={i} className="border-b border-stone-100">
                {columns.map((col) => (
                  <td key={col.key} className="px-5 py-3">
                    <Skeleton variant="line" className="h-4 w-full" />
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <EmptyState
        icon={Inbox}
        title={t("common.noData")}
        description={resolvedEmptyMessage}
      />
    );
  }

  return (
    <div className="w-full overflow-x-auto rounded-xl border border-stone-200/60 bg-white">
      <table className="w-full text-sm">
        <thead className="bg-stone-50 text-xs font-medium uppercase tracking-wider text-stone-500">
          <tr>
            {columns.map((col) => (
              <th key={col.key} className="px-5 py-3 text-left" style={{ width: col.width }}>
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, idx) => (
            <tr
              key={idx}
              className={cn(
                "border-b border-stone-100 transition-colors hover:bg-stone-50/50",
                onRowClick && "cursor-pointer",
                rowClassName?.(row)
              )}
              onClick={() => onRowClick?.(row)}
            >
              {columns.map((col) => (
                <td key={col.key} className="px-5 py-3">
                  {col.render
                    ? col.render(row)
                    : String((row[col.key] as React.ReactNode) ?? "")}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      {pagination && pagination.totalPages > 1 && (
        <div className="flex items-center justify-center gap-1 border-t border-stone-100 px-5 py-3">
          <button
            type="button"
            className="h-8 w-8 rounded-lg border border-stone-200 bg-white text-sm font-medium text-stone-600 hover:bg-stone-50 disabled:opacity-50"
            disabled={pagination.page <= 1}
            onClick={() => pagination.onPageChange(pagination.page - 1)}
          >
            ←
          </button>
          <span className="px-3 text-sm text-stone-500">
            {pagination.page} / {pagination.totalPages}
          </span>
          <button
            type="button"
            className="h-8 w-8 rounded-lg border border-stone-200 bg-white text-sm font-medium text-stone-600 hover:bg-stone-50 disabled:opacity-50"
            disabled={pagination.page >= pagination.totalPages}
            onClick={() => pagination.onPageChange(pagination.page + 1)}
          >
            →
          </button>
        </div>
      )}
    </div>
  );
}
