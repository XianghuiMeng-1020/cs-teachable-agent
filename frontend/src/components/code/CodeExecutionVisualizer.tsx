import { useState, useEffect, useRef } from "react";
import { 
  Play, 
  Pause, 
  SkipForward, 
  SkipBack, 
  RotateCcw,
  Terminal,
  AlertCircle,
  CheckCircle,
  Variable,
  ArrowRight
} from "lucide-react";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { cn } from "@/lib/utils";

interface ExecutionStep {
  line: number;
  variables: Record<string, any>;
  output: string;
  explanation: string;
  highlight_lines: number[];
}

interface CodeExecutionVisualizerProps {
  code: string;
  className?: string;
}

// Simple Python code parser for demo
function parsePythonCode(code: string): ExecutionStep[] {
  const lines = code.split("\n");
  const steps: ExecutionStep[] = [];
  const variables: Record<string, any> = {};
  let output = "";

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    if (!line || line.startsWith("#")) continue;

    // Parse variable assignment
    const assignMatch = line.match(/^(\w+)\s*=\s*(.+)$/);
    if (assignMatch) {
      const [, varName, value] = assignMatch;
      try {
        // Simple evaluation for demo
        if (value.includes("[")) {
          variables[varName] = "[...]"; // List
        } else if (value.startsWith('"') || value.startsWith("'")) {
          variables[varName] = value.slice(1, -1); // String
        } else if (!isNaN(Number(value))) {
          variables[varName] = Number(value); // Number
        } else {
          variables[varName] = value;
        }
      } catch {
        variables[varName] = value;
      }
    }

    // Parse print statements
    const printMatch = line.match(/print\s*\((.+)\)/);
    if (printMatch) {
      const content = printMatch[1];
      if (variables[content]) {
        output += String(variables[content]) + "\n";
      } else {
        output += content.replace(/['"]/g, "") + "\n";
      }
    }

    steps.push({
      line: i,
      variables: { ...variables },
      output: output,
      explanation: getExplanation(line, variables),
      highlight_lines: [i],
    });
  }

  return steps;
}

function getExplanation(line: string, variables: Record<string, any>): string {
  if (line.includes("=") && !line.includes("==")) {
    const varName = line.split("=")[0].trim();
    return `Variable '${varName}' is assigned a value and stored in memory.`;
  }
  if (line.includes("print")) {
    return "The print function outputs text to the console.";
  }
  if (line.includes("for")) {
    return "A for loop begins, which will iterate over the specified range.";
  }
  if (line.includes("if")) {
    return "An if statement checks a condition before executing the code block.";
  }
  return "This line of code is executed.";
}

export function CodeExecutionVisualizer({ code, className }: CodeExecutionVisualizerProps) {
  const [steps, setSteps] = useState<ExecutionStep[]>([]);
  const [currentStep, setCurrentStep] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [speed, setSpeed] = useState(1000);
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    const parsed = parsePythonCode(code);
    setSteps(parsed);
    setCurrentStep(0);
  }, [code]);

  useEffect(() => {
    if (isPlaying && currentStep < steps.length - 1) {
      timerRef.current = setTimeout(() => {
        setCurrentStep((prev) => prev + 1);
      }, speed);
    } else if (currentStep >= steps.length - 1) {
      setIsPlaying(false);
    }

    return () => {
      if (timerRef.current) {
        clearTimeout(timerRef.current);
      }
    };
  }, [isPlaying, currentStep, steps.length, speed]);

  const current = steps[currentStep];

  const handlePlay = () => setIsPlaying(!isPlaying);
  const handleNext = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep((prev) => prev + 1);
    }
  };
  const handlePrev = () => {
    if (currentStep > 0) {
      setCurrentStep((prev) => prev - 1);
    }
  };
  const handleReset = () => {
    setIsPlaying(false);
    setCurrentStep(0);
  };

  if (steps.length === 0) {
    return (
      <Card padding="md" className={className}>
        <p className="text-slate-500">No executable code to visualize.</p>
      </Card>
    );
  }

  return (
    <Card padding="none" className={cn("overflow-hidden", className)}>
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-slate-200 bg-slate-50">
        <div className="flex items-center gap-2">
          <Terminal className="w-5 h-5 text-brand-600" />
          <span className="font-semibold text-slate-900">Code Execution Visualizer</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-500">
            Step {currentStep + 1} of {steps.length}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-0">
        {/* Code Panel */}
        <div className="border-r border-slate-200">
          <div className="relative">
            {/* Line numbers with highlighting */}
            <div className="absolute left-0 top-0 bottom-0 w-12 bg-slate-100 border-r border-slate-200">
              {code.split("\n").map((_, i) => (
                <div
                  key={i}
                  className={cn(
                    "h-6 flex items-center justify-center text-xs",
                    current?.highlight_lines?.includes(i)
                      ? "bg-brand-100 text-brand-700 font-bold"
                      : "text-slate-400"
                  )}
                >
                  {i + 1}
                </div>
              ))}
            </div>
            
            {/* Code with syntax highlighting */}
            <div className="pl-12">
              <SyntaxHighlighter
                language="python"
                style={oneDark}
                customStyle={{
                  margin: 0,
                  padding: "0 1rem",
                  fontSize: "0.875rem",
                  lineHeight: "1.5rem",
                  background: "transparent",
                }}
                showLineNumbers={false}
              >
                {code}
              </SyntaxHighlighter>
            </div>

            {/* Execution pointer */}
            {current && (
              <div
                className="absolute left-0 right-0 h-6 bg-brand-500/10 border-l-4 border-brand-500 pointer-events-none transition-all"
                style={{ top: `${current.line * 1.5}rem` }}
              />
            )}
          </div>

          {/* Controls */}
          <div className="flex items-center gap-2 p-4 border-t border-slate-200 bg-slate-50">
            <Button
              size="sm"
              variant="outline"
              onClick={handleReset}
              icon={RotateCcw}
            >
              Reset
            </Button>
            <Button
              size="sm"
              variant={isPlaying ? "secondary" : "primary"}
              onClick={handlePlay}
              icon={isPlaying ? Pause : Play}
            >
              {isPlaying ? "Pause" : "Play"}
            </Button>
            <Button
              size="sm"
              variant="outline"
              onClick={handlePrev}
              disabled={currentStep === 0}
              icon={SkipBack}
            />
            <Button
              size="sm"
              variant="outline"
              onClick={handleNext}
              disabled={currentStep === steps.length - 1}
              icon={SkipForward}
            />
            
            <div className="flex-1" />
            
            {/* Speed control */}
            <select
              value={speed}
              onChange={(e) => setSpeed(Number(e.target.value))}
              className="text-sm border border-slate-200 rounded px-2 py-1"
            >
              <option value={2000}>Slow</option>
              <option value={1000}>Normal</option>
              <option value={500}>Fast</option>
            </select>
          </div>

          {/* Progress bar */}
          <div className="h-1 bg-slate-200">
            <div
              className="h-full bg-brand-500 transition-all"
              style={{ width: `${((currentStep + 1) / steps.length) * 100}%` }}
            />
          </div>
        </div>

        {/* State Panel */}
        <div className="p-4 space-y-4">
          {/* Explanation */}
          {current && (
            <div className="p-3 bg-brand-50 rounded-lg border border-brand-100">
              <div className="flex items-start gap-2">
                <ArrowRight className="w-4 h-4 text-brand-600 mt-0.5" />
                <p className="text-sm text-brand-800">{current.explanation}</p>
              </div>
            </div>
          )}

          {/* Variables */}
          <div>
            <h4 className="text-sm font-medium text-slate-700 mb-2 flex items-center gap-2">
              <Variable className="w-4 h-4" />
              Variables
            </h4>
            {current && Object.keys(current.variables).length > 0 ? (
              <div className="space-y-2">
                {Object.entries(current.variables).map(([name, value]) => (
                  <div
                    key={name}
                    className="flex items-center justify-between p-2 bg-slate-50 rounded-lg"
                  >
                    <code className="text-sm font-mono text-brand-600">{name}</code>
                    <code className="text-sm font-mono text-slate-700">
                      {typeof value === "string" ? `"${value}"` : String(value)}
                    </code>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-sm text-slate-400">No variables defined yet</p>
            )}
          </div>

          {/* Output */}
          <div>
            <h4 className="text-sm font-medium text-slate-700 mb-2 flex items-center gap-2">
              <Terminal className="w-4 h-4" />
              Console Output
            </h4>
            <div className="p-3 bg-slate-900 rounded-lg min-h-[100px]">
              {current?.output ? (
                <pre className="text-sm font-mono text-emerald-400 whitespace-pre-wrap">
                  {current.output}
                </pre>
              ) : (
                <span className="text-sm text-slate-500">(no output yet)</span>
              )}
            </div>
          </div>

          {/* Step info */}
          <div className="flex items-center justify-between text-xs text-slate-500 pt-2 border-t border-slate-200">
            <span>Line {current ? current.line + 1 : 0}</span>
            <span className={cn(
              currentStep === steps.length - 1 ? "text-emerald-600 font-medium" : ""
            )}>
              {currentStep === steps.length - 1 ? "Execution Complete" : "Running..."}
            </span>
          </div>
        </div>
      </div>
    </Card>
  );
}
