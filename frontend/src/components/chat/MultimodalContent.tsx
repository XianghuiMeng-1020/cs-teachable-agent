import { useState, useEffect } from "react";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import { 
  Image, 
  BarChart3, 
  Code2, 
  Maximize2, 
  X,
  Play,
  Copy,
  Check,
  AlertCircle
} from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";

interface CodeBlock {
  type: "code";
  language: string;
  code: string;
  filename?: string;
}

interface ImageBlock {
  type: "image";
  src: string;
  alt: string;
  caption?: string;
}

interface ChartBlock {
  type: "chart";
  chartType: "bar" | "line" | "pie" | "flow";
  data: unknown;
  title?: string;
}

interface TextBlock {
  type: "text";
  content: string;
}

type ContentBlock = CodeBlock | ImageBlock | ChartBlock | TextBlock;

interface MultimodalContentProps {
  content: string;
  className?: string;
}

// Parse content into multimodal blocks
function parseContent(content: string): ContentBlock[] {
  const blocks: ContentBlock[] = [];
  let remaining = content;
  
  // Regex patterns
  const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g;
  const imageRegex = /!\[([^\]]*)\]\(([^)]+)\)/g;
  const chartRegex = /\[chart:(\w+)\]\n([\s\S]*?)\[\/chart\]/g;
  
  let lastIndex = 0;
  const matches: Array<{ index: number; length: number; block: ContentBlock }> = [];
  
  // Find code blocks
  let match;
  while ((match = codeBlockRegex.exec(content)) !== null) {
    matches.push({
      index: match.index,
      length: match[0].length,
      block: {
        type: "code",
        language: match[1] || "text",
        code: match[2].trim(),
      } as CodeBlock,
    });
  }
  
  // Find images
  imageRegex.lastIndex = 0;
  while ((match = imageRegex.exec(content)) !== null) {
    matches.push({
      index: match.index,
      length: match[0].length,
      block: {
        type: "image",
        alt: match[1],
        src: match[2],
      } as ImageBlock,
    });
  }
  
  // Find charts
  chartRegex.lastIndex = 0;
  while ((match = chartRegex.exec(content)) !== null) {
    try {
      const data = JSON.parse(match[2].trim());
      matches.push({
        index: match.index,
        length: match[0].length,
        block: {
          type: "chart",
          chartType: match[1] as ChartBlock["chartType"],
          data,
        } as ChartBlock,
      });
    } catch {
      // Invalid JSON, skip
    }
  }
  
  // Sort by index
  matches.sort((a, b) => a.index - b.index);
  
  // Build blocks
  let currentIndex = 0;
  for (const m of matches) {
    if (m.index > currentIndex) {
      const textContent = content.slice(currentIndex, m.index).trim();
      if (textContent) {
        blocks.push({ type: "text", content: textContent });
      }
    }
    blocks.push(m.block);
    currentIndex = m.index + m.length;
  }
  
  // Add remaining text
  if (currentIndex < content.length) {
    const textContent = content.slice(currentIndex).trim();
    if (textContent) {
      blocks.push({ type: "text", content: textContent });
    }
  }
  
  // If no blocks, treat entire content as text
  if (blocks.length === 0) {
    blocks.push({ type: "text", content });
  }
  
  return blocks;
}

// Code block component with syntax highlighting
function CodeBlockView({ block, onRun }: { block: CodeBlock; onRun?: (code: string) => void }) {
  const [copied, setCopied] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);
  
  const handleCopy = async () => {
    await navigator.clipboard.writeText(block.code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };
  
  const lineCount = block.code.split("\n").length;
  const shouldCollapse = lineCount > 15 && !isExpanded;
  const displayCode = shouldCollapse ? block.code.split("\n").slice(0, 15).join("\n") + "\n..." : block.code;
  
  return (
    <div className="my-3 rounded-lg overflow-hidden border border-stone-700 bg-[#282c34]">
      {/* Header */}
      <div className="flex items-center justify-between px-3 py-2 bg-[#21252b] border-b border-stone-700">
        <div className="flex items-center gap-2">
          <Code2 className="w-4 h-4 text-stone-400" />
          <span className="text-xs text-stone-300 font-medium">
            {block.language}
          </span>
          {block.filename && (
            <span className="text-xs text-stone-500">{block.filename}</span>
          )}
        </div>
        <div className="flex items-center gap-1">
          {onRun && block.language === "python" && (
            <button
              onClick={() => onRun(block.code)}
              className="p-1.5 rounded hover:bg-stone-700 text-stone-400 hover:text-emerald-400 transition-colors"
              title="Run code"
            >
              <Play className="w-4 h-4" />
            </button>
          )}
          <button
            onClick={handleCopy}
            className="p-1.5 rounded hover:bg-stone-700 text-stone-400 hover:text-white transition-colors"
            title="Copy code"
          >
            {copied ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
          </button>
          {lineCount > 15 && (
            <button
              onClick={() => setIsExpanded(!isExpanded)}
              className="p-1.5 rounded hover:bg-stone-700 text-stone-400 hover:text-white transition-colors"
              title={isExpanded ? "Collapse" : "Expand"}
            >
              {isExpanded ? <X className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
            </button>
          )}
        </div>
      </div>
      
      {/* Code */}
      <SyntaxHighlighter
        language={block.language === "py" ? "python" : block.language}
        style={oneDark}
        customStyle={{
          margin: 0,
          padding: "1rem",
          fontSize: "0.875rem",
          lineHeight: "1.5",
          background: "transparent",
        }}
        showLineNumbers
        lineNumberStyle={{ color: "#495162", minWidth: "2.5em" }}
      >
        {displayCode}
      </SyntaxHighlighter>
      
      {/* Expand hint */}
      {shouldCollapse && (
        <div className="px-3 py-2 bg-[#21252b] border-t border-stone-700 text-center">
          <button
            onClick={() => setIsExpanded(true)}
            className="text-xs text-stone-400 hover:text-white transition-colors"
          >
            Show {lineCount - 15} more lines
          </button>
        </div>
      )}
    </div>
  );
}

// Image block component
function ImageBlockView({ block }: { block: ImageBlock }) {
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);
  
  return (
    <div className="my-3">
      <Card padding="none" className="overflow-hidden">
        {isLoading && !error && (
          <div className="h-48 bg-stone-100 animate-pulse flex items-center justify-center">
            <Image className="w-8 h-8 text-stone-300" />
          </div>
        )}
        
        {error && (
          <div className="h-48 bg-stone-50 flex items-center justify-center">
            <div className="text-center">
              <AlertCircle className="w-8 h-8 text-stone-300 mx-auto mb-2" />
              <p className="text-sm text-stone-500">Failed to load image</p>
            </div>
          </div>
        )}
        
        <img
          src={block.src}
          alt={block.alt}
          className={`w-full h-auto max-h-[400px] object-contain ${isLoading || error ? "hidden" : ""} ${isExpanded ? "max-h-none" : ""}`}
          onLoad={() => setIsLoading(false)}
          onError={() => { setIsLoading(false); setError(true); }}
          onClick={() => setIsExpanded(!isExpanded)}
        />
        
        {(block.alt || block.caption) && (
          <div className="px-3 py-2 bg-stone-50 border-t border-stone-100">
            <p className="text-sm text-stone-600">{block.caption || block.alt}</p>
          </div>
        )}
      </Card>
    </div>
  );
}

// Simple chart visualization
function ChartBlockView({ block }: { block: ChartBlock }) {
  const chartData = block.data as { labels: string[]; values: number[]; title?: string };
  
  const maxValue = Math.max(...(chartData.values || []));
  
  return (
    <Card padding="md" className="my-3">
      <div className="flex items-center gap-2 mb-4">
        <BarChart3 className="w-5 h-5 text-brand-500" />
        <span className="font-medium text-stone-900">{chartData.title || block.title || "Chart"}</span>
      </div>
      
      <div className="space-y-3">
        {chartData.labels?.map((label, index) => {
          const value = chartData.values[index] || 0;
          const percentage = maxValue > 0 ? (value / maxValue) * 100 : 0;
          
          return (
            <div key={label}>
              <div className="flex items-center justify-between text-sm mb-1">
                <span className="text-stone-700">{label}</span>
                <span className="font-medium text-stone-900">{value}</span>
              </div>
              <div className="h-2 bg-stone-100 rounded-full overflow-hidden">
                <div
                  className="h-full bg-brand-500 rounded-full transition-all duration-500"
                  style={{ width: `${percentage}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </Card>
  );
}

// Text block with markdown-like formatting
function TextBlockView({ content }: { content: string }) {
  // Simple formatting: bold, italic, inline code
  const formatted = content
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.+?)\*/g, "<em>$1</em>")
    .replace(/`(.+?)`/g, '<code class="px-1.5 py-0.5 bg-stone-100 rounded text-sm font-mono text-brand-600">$1</code>');
  
  return (
    <div 
      className="prose prose-slate prose-sm max-w-none"
      dangerouslySetInnerHTML={{ __html: formatted.replace(/\n/g, "<br />") }}
    />
  );
}

// Main component
export function MultimodalContent({ content, className }: MultimodalContentProps) {
  const [blocks, setBlocks] = useState<ContentBlock[]>([]);
  const [runResult, setRunResult] = useState<{ code: string; output: string; error?: string } | null>(null);
  
  useEffect(() => {
    setBlocks(parseContent(content));
  }, [content]);
  
  const handleRunCode = async (code: string) => {
    setRunResult({ code, output: "Running..." });
    
    try {
      // Call the sandbox API to run Python code
      const response = await fetch("/api/sandbox/run-python", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code }),
      });
      
      const result = await response.json();
      
      if (result.returncode === 0) {
        setRunResult({ code, output: result.stdout || "(No output)" });
      } else {
        setRunResult({ 
          code, 
          output: result.stdout || "", 
          error: result.stderr || "Runtime error" 
        });
      }
    } catch (err) {
      setRunResult({ 
        code, 
        output: "", 
        error: err instanceof Error ? err.message : "Failed to run code" 
      });
    }
  };
  
  return (
    <div className={className}>
      {blocks.map((block, index) => {
        switch (block.type) {
          case "code":
            return <CodeBlockView key={index} block={block} onRun={handleRunCode} />;
          case "image":
            return <ImageBlockView key={index} block={block} />;
          case "chart":
            return <ChartBlockView key={index} block={block} />;
          case "text":
            return <TextBlockView key={index} content={block.content} />;
          default:
            return null;
        }
      })}
      
      {/* Code execution result modal */}
      {runResult && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
          <Card padding="lg" className="w-full max-w-2xl max-h-[80vh] overflow-auto">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-semibold text-stone-900">Code Execution Result</h3>
              <button
                onClick={() => setRunResult(null)}
                className="p-1 hover:bg-stone-100 rounded"
              >
                <X className="w-5 h-5 text-stone-500" />
              </button>
            </div>
            
            <div className="space-y-4">
              <div>
                <p className="text-xs text-stone-500 mb-1">Code:</p>
                <pre className="p-3 bg-stone-100 rounded-lg text-sm font-mono overflow-x-auto">
                  {runResult.code}
                </pre>
              </div>
              
              {runResult.error ? (
                <div>
                  <p className="text-xs text-rose-500 mb-1">Error:</p>
                  <pre className="p-3 bg-rose-50 text-rose-700 rounded-lg text-sm font-mono overflow-x-auto">
                    {runResult.error}
                  </pre>
                </div>
              ) : (
                <div>
                  <p className="text-xs text-emerald-600 mb-1">Output:</p>
                  <pre className="p-3 bg-emerald-50 text-emerald-900 rounded-lg text-sm font-mono overflow-x-auto whitespace-pre-wrap">
                    {runResult.output}
                  </pre>
                </div>
              )}
            </div>
          </Card>
        </div>
      )}
    </div>
  );
}
