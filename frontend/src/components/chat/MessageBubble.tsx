import { motion } from "framer-motion";
import { Bot } from "lucide-react";
import { cn } from "@/lib/utils";

export interface MessageBubbleProps {
  role: "student" | "ta";
  content: string;
  timestamp?: string;
  metadata?: { interpreted_units?: string[]; quality_score?: number };
}

export function MessageBubble({ role, content, timestamp, metadata }: MessageBubbleProps) {
  const isStudent = role === "student";

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25 }}
      className={cn("flex gap-2", isStudent && "flex-row-reverse")}
    >
      {!isStudent && (
        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-accent-500 text-white">
          <Bot className="h-4 w-4" />
        </div>
      )}
      <div className={cn("flex max-w-[80%] flex-col", isStudent && "items-end")}>
        <div
          className={cn(
            "rounded-2xl px-4 py-2.5",
            isStudent
              ? "rounded-br-md bg-brand-500 text-white"
              : "rounded-bl-md bg-slate-100 text-slate-800"
          )}
        >
          <p className="whitespace-pre-wrap text-sm">{content}</p>
        </div>
        {timestamp && (
          <p className={cn("mt-1 text-[11px] text-slate-400", isStudent && "text-right")}>
            {timestamp}
          </p>
        )}
        {!isStudent && metadata?.interpreted_units?.length && (
          <p className="mt-1 text-xs text-slate-400">
            Learned: {metadata.interpreted_units.join(", ")}
            {metadata.quality_score != null && ` · quality ${metadata.quality_score}`}
          </p>
        )}
      </div>
    </motion.div>
  );
}
