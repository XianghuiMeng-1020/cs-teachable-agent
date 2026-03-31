import { useState } from "react";
import { Info, GitCompare } from "lucide-react";
import { cn } from "@/lib/utils";
import { teach } from "@/api/client";
import { Button } from "@/components/ui/Button";

export function ModelComparison({ taId, className }: { taId: number | null; className?: string }) {
  const [prompt, setPrompt] = useState("");
  const [responseA, setResponseA] = useState("");
  const [responseB, setResponseB] = useState("");
  const [loading, setLoading] = useState(false);

  const handleCompare = async () => {
    if (!taId || !prompt.trim()) return;
    setLoading(true);
    setResponseA("");
    setResponseB("");
    try {
      const [res1, res2] = await Promise.all([teach(taId, prompt.trim()), teach(taId, prompt.trim())]);
      setResponseA(res1?.ta_response ?? "");
      setResponseB(res2?.ta_response ?? "");
    } catch (e) {
      setResponseA("Error: " + (e instanceof Error ? e.message : "Failed"));
      setResponseB("");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={cn("rounded-xl border border-stone-200 bg-stone-50/80 p-4", className)}>
      <h3 className="flex items-center gap-2 text-sm font-semibold text-stone-700">
        <GitCompare className="h-4 w-4" />
        Model comparison
      </h3>
      <p className="mt-1 text-xs text-stone-500">
        Same prompt, two responses: see how the TA can vary between calls (temperature / sampling).
      </p>
      <textarea
        placeholder="Enter a teaching prompt..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        className="mt-3 w-full rounded border border-stone-300 bg-white p-2 text-sm min-h-[60px]"
        disabled={!taId}
      />
      <Button
        onClick={handleCompare}
        disabled={!taId || !prompt.trim() || loading}
        className="mt-2"
      >
        {loading ? "Comparing..." : "Compare (run twice)"}
      </Button>
      {(responseA || responseB) && (
        <div className="mt-4 grid grid-cols-2 gap-3">
          <div className="rounded border border-stone-200 bg-white p-2 text-sm">
            <p className="text-xs font-medium text-stone-500 mb-1">Response A</p>
            <p className="text-stone-700 whitespace-pre-wrap">{responseA || "—"}</p>
          </div>
          <div className="rounded border border-stone-200 bg-white p-2 text-sm">
            <p className="text-xs font-medium text-stone-500 mb-1">Response B</p>
            <p className="text-stone-700 whitespace-pre-wrap">{responseB || "—"}</p>
          </div>
        </div>
      )}
    </div>
  );
}
