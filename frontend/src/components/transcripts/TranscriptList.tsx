import { useState } from "react";
import { useQuery, keepPreviousData } from "@tanstack/react-query";
import { teacherTranscripts } from "@/api/client";
import { DataTable } from "@/components/ui/DataTable";
import { Avatar } from "@/components/ui/Avatar";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Badge } from "@/components/ui/Badge";
import { ExportCSVButton } from "./ExportCSVButton";
import { formatDate } from "@/lib/utils";
import type { TranscriptSessionSummary } from "@/api/client";

interface TranscriptListProps {
  onSelectSession: (sessionId: number) => void;
}

export function TranscriptList({ onSelectSession }: TranscriptListProps) {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [dateFrom, setDateFrom] = useState("");
  const [dateTo, setDateTo] = useState("");
  const [kuFilter, setKuFilter] = useState("");

  const { data, isLoading } = useQuery({
    queryKey: ["teacher", "transcripts", page, search, dateFrom, dateTo, kuFilter],
    queryFn: () =>
      teacherTranscripts({
        page,
        per_page: 10,
        search: search.trim() || undefined,
        date_from: dateFrom || undefined,
        date_to: dateTo || undefined,
        ku: kuFilter.trim() || undefined,
      }),
    placeholderData: keepPreviousData,
  });

  const columns = [
    { key: "session_id", header: "#", width: "80px", render: (r: TranscriptSessionSummary) => r.session_id },
    {
      key: "student",
      header: "Student",
      render: (r: TranscriptSessionSummary) => (
        <div className="flex items-center gap-2">
          <Avatar fallback={r.student.username} size="sm" />
          <span>{r.student.username}</span>
        </div>
      ),
    },
    { key: "message_count", header: "Messages", render: (r: TranscriptSessionSummary) => r.message_count },
    {
      key: "kus_covered",
      header: "KUs Covered",
      render: (r: TranscriptSessionSummary) => (
        <div className="flex flex-wrap gap-1">
          {(r.kus_covered.slice(0, 3) || []).map((ku) => (
            <Badge key={ku} variant="outline" size="sm">{ku}</Badge>
          ))}
          {r.kus_covered.length > 3 && <span className="text-xs text-slate-500">+{r.kus_covered.length - 3} more</span>}
        </div>
      ),
    },
    { key: "started_at", header: "Date", render: (r: TranscriptSessionSummary) => formatDate(r.started_at) },
    {
      key: "actions",
      header: "Actions",
      render: (r: TranscriptSessionSummary) => (
        <Button variant="outline" size="sm" onClick={() => onSelectSession(r.session_id)}>View</Button>
      ),
    },
  ];

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <h1 className="text-2xl font-bold text-slate-900">Teaching Sessions</h1>
        <ExportCSVButton />
      </div>
      <div className="flex flex-wrap items-center gap-3">
        <Input
          placeholder="Search by student name..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="max-w-[200px]"
          aria-label="Search transcripts by student"
        />
        <label className="flex items-center gap-2 text-sm text-slate-600">
          From
          <input
            type="date"
            value={dateFrom}
            onChange={(e) => setDateFrom(e.target.value)}
            className="rounded border border-slate-300 px-2 py-1.5 text-sm"
            aria-label="Filter from date"
          />
        </label>
        <label className="flex items-center gap-2 text-sm text-slate-600">
          To
          <input
            type="date"
            value={dateTo}
            onChange={(e) => setDateTo(e.target.value)}
            className="rounded border border-slate-300 px-2 py-1.5 text-sm"
            aria-label="Filter to date"
          />
        </label>
        <Input
          placeholder="KU filter (comma-separated ids)"
          value={kuFilter}
          onChange={(e) => setKuFilter(e.target.value)}
          className="max-w-[240px]"
          aria-label="Filter by knowledge unit ids"
        />
      </div>
      <DataTable<TranscriptSessionSummary>
        columns={columns}
        data={data?.items ?? []}
        loading={isLoading}
        emptyMessage="No sessions yet."
        pagination={
          data && data.total > data.per_page
            ? { page: data.page, totalPages: Math.ceil(data.total / data.per_page), onPageChange: setPage }
            : undefined
        }
        onRowClick={(r) => onSelectSession(r.session_id)}
      />
    </div>
  );
}
