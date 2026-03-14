import { useState } from "react";
import { Download } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { teacherTranscriptsExport } from "@/api/client";
import { toast } from "sonner";

interface ExportCSVButtonProps {
  sessionId?: number;
}

export function ExportCSVButton({ sessionId }: ExportCSVButtonProps) {
  const [loading, setLoading] = useState(false);

  const handleExport = async () => {
    setLoading(true);
    try {
      const blob = await teacherTranscriptsExport(sessionId);
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = sessionId ? `transcript-${sessionId}.csv` : "transcripts.csv";
      a.click();
      URL.revokeObjectURL(url);
      toast.success("Export started");
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Export failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Button variant="outline" size="sm" icon={Download} loading={loading} onClick={handleExport}>
      Export CSV
    </Button>
  );
}
