import { useTranslation } from "react-i18next";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { MISCONCEPTION_DISPLAY } from "@/lib/constants";

interface MisconceptionRankingProps {
  counts: Record<string, number>;
}

export function MisconceptionRanking({ counts }: MisconceptionRankingProps) {
  const { t } = useTranslation();
  const data = Object.entries(counts)
    .map(([id, count]) => ({ name: MISCONCEPTION_DISPLAY[id] ?? id, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 10);

  if (data.length === 0) {
    return <p className="py-4 text-center text-sm text-stone-500">{t("teacher.noMisconceptions")}</p>;
  }

  return (
    <div className="h-64">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} layout="vertical" margin={{ left: 80 }}>
          <XAxis type="number" />
          <YAxis type="category" dataKey="name" width={76} tick={{ fontSize: 11 }} />
          <Tooltip />
          <Bar dataKey="count" fill="#EF4444" radius={[0, 2, 2, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
