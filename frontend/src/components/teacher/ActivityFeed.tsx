import { Avatar } from "@/components/ui/Avatar";
import { formatRelative } from "@/lib/utils";

export interface ActivityItem {
  student: string;
  action: string;
  result?: string | null;
  timestamp: string;
}

interface ActivityFeedProps {
  items: ActivityItem[];
}

export function ActivityFeed({ items }: ActivityFeedProps) {
  return (
    <ul className="space-y-3">
      {items.slice(0, 20).map((item, i) => (
        <li key={i} className="flex items-start gap-3 rounded-lg border border-slate-100 p-2">
          <Avatar fallback={item.student.slice(0, 2)} size="sm" className="shrink-0" />
          <div className="min-w-0 flex-1">
            <p className="text-sm text-slate-800">
              <span className="font-medium">{item.student}</span>
              {" "}{item.action}
              {item.result != null && item.result !== "" && (
                <span className="text-slate-500"> — {item.result}</span>
              )}
            </p>
            <p className="mt-0.5 text-xs text-slate-400">{formatRelative(item.timestamp)}</p>
          </div>
        </li>
      ))}
      {items.length === 0 && (
        <p className="py-4 text-center text-sm text-slate-500">No recent activity.</p>
      )}
    </ul>
  );
}
