import { useState, useMemo } from "react";
import { useTranslation } from "react-i18next";
import { Send, Lightbulb } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { teach } from "@/api/client";
import { cn } from "@/lib/utils";

interface PromptLabProps {
  taId: number | null;
  className?: string;
}

export function PromptLab({ taId, className }: PromptLabProps) {
  const { t } = useTranslation();
  const tips = useMemo(
    () => [
      t("aiLab.tip1", {
        defaultValue: "Be specific: e.g. 'Explain what a variable is in Python'",
      }),
      t("aiLab.tip2", {
        defaultValue: "Ask for examples: 'Give me 2 examples of loops'",
      }),
      t("aiLab.tip3", {
        defaultValue: "Check understanding: 'What is the difference between = and ==?'",
      }),
    ],
    [t]
  );
  const [prompt, setPrompt] = useState("");
  const [output, setOutput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleRun = async () => {
    if (!taId || !prompt.trim()) return;
    setLoading(true);
    setOutput("");
    try {
      const res = await teach(taId, prompt.trim());
      setOutput(res.ta_response ?? t("aiLab.noResponse", { defaultValue: "(no response)" }));
    } catch (err) {
      setOutput(
        `${t("aiLab.errorLabel", { defaultValue: "Error" })}: ${err instanceof Error ? err.message : t("aiLab.failed", { defaultValue: "Failed" })}`
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={cn("rounded-xl border border-stone-200 bg-white p-4", className)}>
      <h3 className="flex items-center gap-2 text-sm font-semibold text-stone-800">
        <Lightbulb className="h-4 w-4 text-amber-500" />
        {t("aiLab.promptLabTitle", { defaultValue: "Prompt lab" })}
      </h3>
      <p className="mt-1 text-xs text-stone-500">
        {t("aiLab.promptLabDesc")}
      </p>
      <textarea
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder={t("aiLab.promptPlaceholder")}
        className="mt-3 w-full resize-y rounded-lg border border-stone-200 px-3 py-2 text-sm focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 focus:outline-none"
        rows={3}
        disabled={!taId || loading}
      />
      <Button
        icon={Send}
        size="sm"
        className="mt-2"
        onClick={handleRun}
        disabled={!taId || !prompt.trim() || loading}
        loading={loading}
      >
        {t("aiLab.runPrompt", { defaultValue: "Run prompt" })}
      </Button>
      {output && (
        <div className="mt-3 rounded-lg border border-stone-100 bg-stone-50 p-3">
          <p className="text-xs font-medium text-stone-500">
            {t("aiLab.responseLabel", { defaultValue: "Response" })}
          </p>
          <p className="mt-1 whitespace-pre-wrap text-sm text-stone-800">{output}</p>
        </div>
      )}
      <ul className="mt-3 space-y-1 text-xs text-stone-500">
        {tips.map((tip, i) => (
          <li key={i} className="flex gap-2">
            <span className="text-amber-500">•</span>
            {tip}
          </li>
        ))}
      </ul>
    </div>
  );
}
