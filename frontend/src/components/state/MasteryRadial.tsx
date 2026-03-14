import { PieChart, Pie, Cell, ResponsiveContainer } from "recharts";

interface MasteryRadialProps {
  learnedCount: number;
  totalCount: number;
  className?: string;
}

const LEARNED_COLOR = "#06B6D4"; // accent-500
const REMAINING_COLOR = "#e2e8f0"; // slate-200

export function MasteryRadial({ learnedCount, totalCount, className = "" }: MasteryRadialProps) {
  const percent = totalCount > 0 ? Math.round((learnedCount / totalCount) * 100) : 0;
  const data = [
    { name: "learned", value: learnedCount, color: LEARNED_COLOR },
    { name: "remaining", value: Math.max(0, totalCount - learnedCount), color: REMAINING_COLOR },
  ].filter((d) => d.value > 0);

  if (data.length === 0) {
    data.push({ name: "remaining", value: 1, color: REMAINING_COLOR });
  }

  return (
    <div className={`relative ${className}`}>
      <div className="h-[140px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={44}
              outerRadius={56}
              paddingAngle={0}
              dataKey="value"
              isAnimationActive
              animationDuration={1000}
              animationEasing="ease-out"
            >
              {data.map((entry, i) => (
                <Cell key={i} fill={entry.color} />
              ))}
            </Pie>
          </PieChart>
        </ResponsiveContainer>
      </div>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-2xl font-bold text-slate-900">{percent}%</span>
        <span className="text-xs text-slate-500">mastery</span>
      </div>
      <p className="mt-2 text-center text-xs text-slate-500">
        {learnedCount}/{totalCount} concepts learned
      </p>
    </div>
  );
}
