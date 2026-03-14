import { Lightbulb, CheckCircle } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { cn } from "@/lib/utils";
import { MISCONCEPTION_DISPLAY } from "@/lib/constants";

export interface MisconceptionCardProps {
  misconceptionId: string;
  description: string;
  affectedUnits: string[];
  remediationHint: string;
  status: "active" | "correcting" | "resolved";
}

const statusBorder = {
  active: "border-l-danger",
  correcting: "border-l-warning",
  resolved: "border-l-success",
};

export function MisconceptionCard({
  misconceptionId,
  description,
  affectedUnits,
  remediationHint,
  status,
}: MisconceptionCardProps) {
  const title = MISCONCEPTION_DISPLAY[misconceptionId] ?? misconceptionId;

  return (
    <Card padding="md" className={cn("border-l-4", statusBorder[status])}>
      <div className="flex items-start justify-between gap-2">
        <h4 className="text-sm font-semibold text-slate-800">{title}</h4>
        <Badge
          variant={status === "active" ? "danger" : status === "resolved" ? "success" : "warning"}
          size="sm"
        >
          {status}
        </Badge>
      </div>
      <p className="mt-2 text-sm text-slate-600">{description}</p>
      {affectedUnits.length > 0 && (
        <div className="mt-2 flex flex-wrap gap-1">
          {affectedUnits.map((u) => (
            <Badge key={u} variant="outline" size="sm">
              {u}
            </Badge>
          ))}
        </div>
      )}
      <div className="mt-3 flex gap-2 rounded-lg bg-amber-50 p-3 text-sm text-amber-800">
        <Lightbulb className="h-4 w-4 shrink-0 mt-0.5" />
        <span>{remediationHint}</span>
      </div>
    </Card>
  );
}

export function MisconceptionCardEmpty() {
  return (
    <Card padding="md" className="border border-slate-200">
      <div className="flex flex-col items-center justify-center py-4 text-center">
        <CheckCircle className="h-10 w-10 text-success" />
        <p className="mt-2 text-sm font-medium text-slate-700">No active misconceptions</p>
        <p className="mt-1 text-xs text-slate-500">TA knowledge state is consistent.</p>
      </div>
    </Card>
  );
}
