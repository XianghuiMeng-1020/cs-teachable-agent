import { useState } from "react";
import { motion } from "framer-motion";
import { Bot, Copy, Check, Code2, Image as ImageIcon } from "lucide-react";
import { cn } from "@/lib/utils";
import { MultimodalContent } from "./MultimodalContent";

export interface MessageBubbleProps {
  role: "student" | "ta";
  content: string;
  timestamp?: string;
  metadata?: { interpreted_units?: string[]; quality_score?: number; failed?: boolean; lastInput?: string };
  onRetry?: () => void;
}

function MessageContent({ content, isStudent }: { content: string; isStudent: boolean }) {
  // For student messages, use simple text rendering
  if (isStudent) {
    return (
      <p className="text-sm whitespace-pre-wrap">{content}</p>
    );
  }
  
  // For TA messages, use rich multimodal rendering
  return <MultimodalContent content={content} />;
}

export function MessageBubble({ role, content, timestamp, metadata, onRetry }: MessageBubbleProps) {
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
            "rounded-2xl px-4 py-2.5 overflow-hidden",
            isStudent
              ? "rounded-br-md bg-brand-500 text-white"
              : "rounded-bl-md bg-stone-100 text-stone-800"
          )}
        >
          <MessageContent content={content} isStudent={isStudent} />
        </div>
        {timestamp && (
          <p className={cn("mt-1 text-[11px] text-stone-400", isStudent && "text-right")}>
            {timestamp}
          </p>
        )}
        {!isStudent && metadata?.interpreted_units?.length && !metadata?.failed && (
          <p className="mt-1 text-xs text-stone-400">
            Learned: {metadata.interpreted_units.join(", ")}
            {metadata.quality_score != null && ` · quality ${metadata.quality_score}`}
          </p>
        )}
        {!isStudent && metadata?.failed && onRetry && (
          <button
            type="button"
            onClick={onRetry}
            className="mt-2 rounded-lg border border-amber-300 bg-amber-50 px-3 py-1.5 text-xs font-medium text-amber-800 hover:bg-amber-100"
          >
            Retry send
          </button>
        )}
      </div>
    </motion.div>
  );
}
