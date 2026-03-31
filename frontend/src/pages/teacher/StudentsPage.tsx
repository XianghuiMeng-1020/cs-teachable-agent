import { useQuery } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import { teacherStudents } from "@/api/client";
import { DataTable } from "@/components/ui/DataTable";
import { Avatar } from "@/components/ui/Avatar";
import { Badge } from "@/components/ui/Badge";
import { Input } from "@/components/ui/Input";
import { ROUTES } from "@/lib/constants";
import { formatRelative } from "@/lib/utils";
import { useState } from "react";

interface StudentRow {
  user_id: number;
  username: string;
  ta_count: number;
  domain_ids: string[];
}

export function StudentsPage() {
  const navigate = useNavigate();
  const [search, setSearch] = useState("");
  const { data: students = [], isLoading } = useQuery({
    queryKey: ["teacher", "students"],
    queryFn: teacherStudents,
  });

  const filtered = search.trim()
    ? students.filter((s: StudentRow) => s.username.toLowerCase().includes(search.toLowerCase()))
    : students;

  const columns = [
    {
      key: "username",
      header: "Student",
      render: (r: StudentRow) => (
        <div className="flex items-center gap-2">
          <Avatar fallback={r.username} size="sm" />
          <span>{r.username}</span>
        </div>
      ),
    },
    { key: "domain_ids", header: "Domain", render: (r: StudentRow) => r.domain_ids?.join(", ") ?? "—" },
    { key: "ta_count", header: "TAs", render: (r: StudentRow) => r.ta_count },
    {
      key: "actions",
      header: "",
      render: (r: StudentRow) => (
        <button
          type="button"
          className="text-sm font-medium text-brand-600 hover:underline"
          onClick={() => navigate(ROUTES.teacher.studentDetail(r.user_id))}
        >
          View
        </button>
      ),
    },
  ];

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold text-stone-900">Students</h1>
      <div className="flex gap-2">
        <Input placeholder="Search..." value={search} onChange={(e) => setSearch(e.target.value)} className="max-w-xs" />
      </div>
      <p className="text-sm text-stone-500">Total: {filtered.length} students</p>
      <DataTable<StudentRow> columns={columns} data={filtered} loading={isLoading} emptyMessage="No students." />
    </div>
  );
}
