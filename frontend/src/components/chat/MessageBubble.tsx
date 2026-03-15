import { useState } from "react";
import { motion } from "framer-motion";
import { Bot, Copy, Check } from "lucide-react";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import ReactMarkdown from "react-markdown";
import { cn } from "@/lib/utils";

export interface MessageBubbleProps {
  role: "student" | "ta";
  content: string;
  timestamp?: string;
  metadata?: { interpreted_units?: string[]; quality_score?: number; failed?: boolean; lastInput?: string };
  onRetry?: () => void;
}

function CodeBlock({ code, lang }: { code: string; lang: string }) {
  const [copied, setCopied] = useState(false);
  const copy = () => {
    navigator.clipboard.writeText(code).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };
  return (
    <div className="relative group">
      <SyntaxHighlighter
        language={lang}
        style={oneDark}
        customStyle={{ margin: 0, borderRadius: 8, fontSize: "0.8rem", paddingTop: "2rem" }}
        codeTagProps={{ style: { fontFamily: "inherit" } }}
        PreTag="div"
      >
        {code}
      </SyntaxHighlighter>
      <button
        type="button"
        onClick={copy}
        className="absolute right-2 top-2 rounded border border-slate-500/50 bg-slate-700/80 px-2 py-1 text-xs text-slate-200 opacity-0 transition group-hover:opacity-100 hover:bg-slate-600/80"
        aria-label="Copy code"
      >
        {copied ? <Check className="h-3 w-3" /> : <Copy className="h-3 w-3" />}
      </button>
    </div>
  );
}

function MessageContent({ content, isStudent }: { content: string; isStudent: boolean }) {
  const parts = content.split(/(```[\s\S]*?```)/g);
  if (parts.length === 1) {
    return (
      <div className="prose prose-sm max-w-none prose-p:whitespace-pre-wrap prose-p:my-0.5 prose-ul:my-1 prose-li:my-0 text-sm">
        <ReactMarkdown
          components={{
            p: ({ children }) => <p className="whitespace-pre-wrap">{children}</p>,
            a: ({ href, children }) => (
              <a href={href} target="_blank" rel="noopener noreferrer" className="text-brand-600 underline">
                {children}
              </a>
            ),
          }}
        >
          {content}
        </ReactMarkdown>
      </div>
    );
  }
  return (
    <div className="space-y-2 text-sm">
      {parts.map((part, i) => {
        if (part.startsWith("```") && part.endsWith("```")) {
          const raw = part.slice(3, -3).trim();
          const firstLine = raw.split("\n")[0] || "";
          const langMatch = firstLine.match(/^(\w+)/);
          const lang = langMatch ? langMatch[1] : "text";
          const code = langMatch ? raw.slice(firstLine.length).replace(/^\n/, "") : raw;
          return <CodeBlock key={i} code={code} lang={lang} />;
        }
        return (
          <div key={i} className="prose prose-sm max-w-none prose-p:my-0.5 prose-ul:my-1 text-inherit">
            <ReactMarkdown
              components={{
                p: ({ children }) => <p className="whitespace-pre-wrap">{children}</p>,
                a: ({ href, children }) => (
                  <a href={href} target="_blank" rel="noopener noreferrer" className="text-brand-600 underline">
                    {children}
                  </a>
                ),
              }}
            >
              {part}
            </ReactMarkdown>
          </div>
        );
      })}
    </div>
  );
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
              : "rounded-bl-md bg-slate-100 text-slate-800"
          )}
        >
          <MessageContent content={content} isStudent={isStudent} />
        </div>
        {timestamp && (
          <p className={cn("mt-1 text-[11px] text-slate-400", isStudent && "text-right")}>
            {timestamp}
          </p>
        )}
        {!isStudent && metadata?.interpreted_units?.length && !metadata?.failed && (
          <p className="mt-1 text-xs text-slate-400">
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
