import { useState } from "react";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import { Copy, Check } from "lucide-react";
import { cn } from "@/lib/utils";

export interface CodeEditorProps {
  code: string;
  language?: string;
  maxHeight?: string;
  showLineNumbers?: boolean;
  copyButton?: boolean;
  className?: string;
}

export function CodeEditor({
  code,
  language = "python",
  maxHeight = "300px",
  showLineNumbers = true,
  copyButton = true,
  className,
}: CodeEditorProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    void navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div
      className={cn(
        "overflow-hidden rounded-lg border border-stone-200 bg-stone-900",
        className
      )}
    >
      <div className="flex items-center justify-between border-b border-stone-700 bg-stone-800 px-3 py-1.5">
        <span className="text-xs text-stone-400">{language}</span>
        {copyButton && (
          <button
            type="button"
            onClick={handleCopy}
            className="flex items-center gap-1.5 rounded px-2 py-1 text-xs text-stone-400 hover:bg-stone-700 hover:text-white"
          >
            {copied ? <Check className="h-3.5 w-3.5" /> : <Copy className="h-3.5 w-3.5" />}
            {copied ? "Copied" : "Copy"}
          </button>
        )}
      </div>
      <div style={{ maxHeight }} className="overflow-y-auto">
        <SyntaxHighlighter
          language={language}
          style={oneDark}
          showLineNumbers={showLineNumbers}
          lineNumberStyle={{ minWidth: "2em", color: "#64748b" }}
          customStyle={{
            margin: 0,
            padding: "0.75rem 1rem",
            fontSize: "0.875rem",
            lineHeight: 1.6,
            background: "transparent",
          }}
          codeTagProps={{ className: "font-mono" }}
        >
          {code}
        </SyntaxHighlighter>
      </div>
    </div>
  );
}
