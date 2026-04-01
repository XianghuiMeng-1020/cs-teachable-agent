import { useTranslation } from "react-i18next";
import { useQuery } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import { teacherStudents } from "@/api/client";
import { DataTable } from "@/components/ui/DataTable";
import { Avatar } from "@/components/ui/Avatar";
import { Input } from "@/components/ui/Input";
import { ROUTES } from "@/lib/constants";
import { useState } from "react";

interface StudentRow {
  user_id: number;
  username: string;
  ta_count: number;
  domain_ids: string[];
}

export function StudentsPage() {
  const { t } = useTranslation();
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
      header: t("teacher.student"),
      render: (r: StudentRow) => (
        <div className="flex items-center gap-2">
          <Avatar fallback={r.username} size="sm" />
          <span>{r.username}</span>
        </div>
      ),
    },
    { key: "domain_ids", header: t("teacher.domain"), render: (r: StudentRow) => r.domain_ids?.join(", ") ?? "—" },
    { key: "ta_count", header: t("teacher.tas"), render: (r: StudentRow) => r.ta_count },
    {
      key: "actions",
      header: "",
      render: (r: StudentRow) => (
        <button
          type="button"
          className="text-sm font-medium text-brand-600 hover:underline"
          onClick={() => navigate(ROUTES.teacher.studentDetail(r.user_id))}
        >
          {t("teacher.view")}
        </button>
      ),
    },
  ];

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold text-stone-900">{t("nav.students")}</h1>
      <div className="flex gap-2">
        <Input placeholder={t("teacher.searchPlaceholder")} value={search} onChange={(e) => setSearch(e.target.value)} className="max-w-xs" />
      </div>
      <p className="text-sm text-stone-500">{t("teacher.totalCount", { count: filtered.length })}</p>
      <DataTable<StudentRow> columns={columns} data={filtered} loading={isLoading} emptyMessage={t("teacher.noStudents")} />
    </div>
  );
}
