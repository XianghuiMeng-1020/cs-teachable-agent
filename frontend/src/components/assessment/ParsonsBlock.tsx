import { useState, useCallback, useMemo, useRef } from "react";
import { useTranslation } from "react-i18next";
import { Shuffle, GripVertical, X } from "lucide-react";
import { cn } from "@/lib/utils";
import { emitTelemetry } from "@/lib/telemetry";

interface ParsonsBlockProps {
  options: string[];
  requiredBlockCount: number;
  selectedBlocks: string[];
  onSelectedChange: (blocks: string[]) => void;
  disabled?: boolean;
  feedback?: { correct: boolean; feedback: string } | null;
  distractors?: string[];
}

function fisherYatesShuffle<T>(arr: T[]): T[] {
  const copy = [...arr];
  for (let i = copy.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

export function ParsonsBlock({
  options,
  requiredBlockCount,
  selectedBlocks,
  onSelectedChange,
  disabled = false,
  feedback,
  distractors = [],
}: ParsonsBlockProps) {
  const { t } = useTranslation();
  const allBlocks = useMemo(() => [...options, ...distractors], [options, distractors]);
  const [poolOrder, setPoolOrder] = useState<string[]>(() => fisherYatesShuffle(allBlocks));
  const [dragState, setDragState] = useState<{
    source: "pool" | "answer";
    blockText: string;
    index: number;
  } | null>(null);
  const [insertIndex, setInsertIndex] = useState<number | null>(null);
  const poolRef = useRef<HTMLDivElement>(null);

  const pool = poolOrder.filter((o) => !selectedBlocks.includes(o));

  const addBlock = useCallback(
    (block: string) => {
      if (disabled) return;
      onSelectedChange([...selectedBlocks, block]);
      emitTelemetry("block_added", { block: block.slice(0, 60) });
    },
    [selectedBlocks, onSelectedChange, disabled]
  );

  const removeBlock = useCallback(
    (index: number) => {
      if (disabled) return;
      const removed = selectedBlocks[index];
      const next = [...selectedBlocks];
      next.splice(index, 1);
      onSelectedChange(next);
      emitTelemetry("block_removed", { block: removed?.slice(0, 60), index });
    },
    [selectedBlocks, onSelectedChange, disabled]
  );

  const shufflePool = () => {
    setPoolOrder(fisherYatesShuffle(allBlocks));
    emitTelemetry("pool_shuffled");
  };

  const handlePoolDragStart = (e: React.DragEvent, block: string, index: number) => {
    e.dataTransfer.effectAllowed = "move";
    setDragState({ source: "pool", blockText: block, index });
  };

  const handleAnswerDragStart = (e: React.DragEvent, block: string, index: number) => {
    e.dataTransfer.effectAllowed = "move";
    setDragState({ source: "answer", blockText: block, index });
  };

  const handleAnswerDragOver = (e: React.DragEvent, index: number) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = "move";
    setInsertIndex(index);
  };

  const handleAnswerDrop = (targetIndex: number) => {
    if (!dragState) return;

    if (dragState.source === "pool") {
      const next = [...selectedBlocks];
      next.splice(targetIndex, 0, dragState.blockText);
      onSelectedChange(next);
      emitTelemetry("block_added", { block: dragState.blockText.slice(0, 60), position: targetIndex });
    } else if (dragState.source === "answer") {
      if (dragState.index === targetIndex) return;
      const next = [...selectedBlocks];
      const [moved] = next.splice(dragState.index, 1);
      const adjustedTarget = dragState.index < targetIndex ? targetIndex - 1 : targetIndex;
      next.splice(adjustedTarget, 0, moved);
      onSelectedChange(next);
      emitTelemetry("block_reordered", { from: dragState.index, to: adjustedTarget });
    }

    setDragState(null);
    setInsertIndex(null);
  };

  const handleDragEnd = () => {
    setDragState(null);
    setInsertIndex(null);
  };

  const handlePoolDrop = () => {
    if (dragState?.source === "answer") {
      removeBlock(dragState.index);
    }
    setDragState(null);
    setInsertIndex(null);
  };

  const handlePoolKeyDown = (e: React.KeyboardEvent, block: string) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      addBlock(block);
    }
  };

  return (
    <div className="space-y-4">
      {/* Pool */}
      <div>
        <div className="mb-2 flex items-center justify-between">
          <h4 className="text-sm font-medium text-stone-500">
            {t("assessment.availableBlocksCount", { count: pool.length })}
          </h4>
          <button
            type="button"
            onClick={shufflePool}
            disabled={disabled || pool.length <= 1}
            className="flex items-center gap-1 rounded-md border border-stone-200 px-2 py-1 text-xs font-medium text-stone-500 hover:bg-stone-50 transition-colors disabled:opacity-40"
          >
            <Shuffle className="h-3 w-3" />
            {t("assessment.shuffle")}
          </button>
        </div>
        <div
          ref={poolRef}
          className={cn(
            "space-y-1.5 rounded-lg border-2 border-dashed p-3 min-h-[60px] transition-colors",
            dragState?.source === "answer" ? "border-amber-400 bg-amber-50/50" : "border-stone-300 bg-stone-50"
          )}
          onDragOver={(e) => { e.preventDefault(); e.dataTransfer.dropEffect = "move"; }}
          onDrop={handlePoolDrop}
        >
          {pool.length === 0 && (
            <p className="text-xs text-stone-400 italic">{t("assessment.allBlocksPlaced")}</p>
          )}
          {pool.map((block, i) => (
            <div
              key={`pool-${block}-${i}`}
              role="button"
              tabIndex={disabled ? -1 : 0}
              draggable={!disabled}
              onDragStart={(e) => handlePoolDragStart(e, block, i)}
              onDragEnd={handleDragEnd}
              onClick={() => addBlock(block)}
              onKeyDown={(e) => handlePoolKeyDown(e, block)}
              className={cn(
                "flex items-center gap-2 w-full rounded-lg border border-stone-200 bg-white px-3 py-2 text-left font-mono text-sm shadow-sm transition-all cursor-pointer",
                "hover:border-brand-400 hover:bg-brand-50 focus:outline-none focus:ring-2 focus:ring-brand-600/20",
                disabled && "cursor-not-allowed opacity-60",
                distractors.includes(block) && "border-stone-200"
              )}
            >
              <GripVertical className="h-3.5 w-3.5 shrink-0 text-stone-300" />
              <pre className="flex-1 whitespace-pre-wrap">{block}</pre>
            </div>
          ))}
        </div>
      </div>

      {/* Answer area */}
      <div>
        <h4 className="mb-2 text-sm font-medium text-stone-500">
          {t("assessment.yourSolutionProgress", {
            current: selectedBlocks.length,
            required: requiredBlockCount,
          })}
        </h4>
        <div className={cn(
          "rounded-lg border-2 p-3 min-h-[80px] transition-colors",
          dragState ? "border-brand-400 bg-brand-50/30" : "border-brand-200 bg-brand-50/20"
        )}>
          {selectedBlocks.length === 0 && !dragState && (
            <p className="text-xs text-stone-400 italic py-2">{t("assessment.dragBlocksHint")}</p>
          )}

          {/* Insertion marker at top */}
          {dragState && (
            <div
              className={cn(
                "h-1 rounded-full mb-1 transition-colors",
                insertIndex === 0 ? "bg-brand-500" : "bg-transparent"
              )}
              onDragOver={(e) => handleAnswerDragOver(e, 0)}
              onDrop={() => handleAnswerDrop(0)}
            />
          )}

          {selectedBlocks.map((block, i) => (
            <div key={`sel-${block}-${i}`}>
              <div
                draggable={!disabled}
                onDragStart={(e) => handleAnswerDragStart(e, block, i)}
                onDragEnd={handleDragEnd}
                className={cn(
                  "group flex items-start gap-2 rounded-lg border bg-white px-3 py-2 font-mono text-sm shadow-sm transition-all",
                  dragState?.source === "answer" && dragState?.index === i && "opacity-40",
                  disabled && "cursor-not-allowed"
                )}
              >
                <GripVertical className="mt-0.5 h-3.5 w-3.5 shrink-0 text-stone-300 cursor-grab" />
                <span className="mt-0.5 select-none text-xs text-stone-400 font-sans w-5 shrink-0">
                  {i + 1}.
                </span>
                <pre className="flex-1 whitespace-pre-wrap">{block}</pre>
                {!disabled && (
                  <button
                    onClick={() => removeBlock(i)}
                    className="mt-0.5 shrink-0 rounded p-0.5 text-stone-400 hover:text-red-500 hover:bg-red-50 transition-colors"
                    aria-label={t("assessment.removeBlock")}
                  >
                    <X className="h-3.5 w-3.5" />
                  </button>
                )}
              </div>
              {/* Insertion marker between blocks */}
              {dragState && (
                <div
                  className={cn(
                    "h-1 rounded-full my-1 transition-colors",
                    insertIndex === i + 1 ? "bg-brand-500" : "bg-transparent"
                  )}
                  onDragOver={(e) => handleAnswerDragOver(e, i + 1)}
                  onDrop={() => handleAnswerDrop(i + 1)}
                />
              )}
            </div>
          ))}
        </div>
      </div>

      {feedback && (
        <div
          className={cn(
            "rounded-xl border px-4 py-3 text-sm",
            feedback.correct
              ? "border-emerald-200 bg-emerald-50 text-emerald-800"
              : "border-amber-200 bg-amber-50 text-amber-800"
          )}
        >
          {feedback.feedback}
        </div>
      )}
    </div>
  );
}
