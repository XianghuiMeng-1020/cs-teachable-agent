import { BuggyCodeBlock } from "./BuggyCodeBlock";
import { OutputPrediction } from "./OutputPrediction";
import { CodeCompletion } from "./CodeCompletion";
import { ConceptMCQ } from "./ConceptMCQ";
import { ShortCodeAnswer } from "./ShortCodeAnswer";
import { ParsonsBlock } from "@/components/assessment/ParsonsBlock";
import { DropdownBlanks } from "@/components/assessment/DropdownBlanks";
import { ExecutionTrace } from "@/components/assessment/ExecutionTrace";
import { Bug, Eye, Code, ListChecks, FileText, Puzzle, Terminal, Brain } from "lucide-react";

export interface TeachProblem {
  problem_id: string;
  problem_type: string;
  problem_statement: string;
  difficulty?: string;
  difficulty_order?: number;
  topic_group?: string;
  knowledge_units_tested?: string[];
  // buggy-code
  code?: string;
  bug_lines?: number[];
  correct_code?: string;
  bug_explanation?: string;
  // output-prediction
  expected_output?: string;
  // code-completion
  code_template?: string;
  completion_slots?: { line: number; placeholder: string }[];
  // multiple-choice
  choices?: { id: string; text: string }[];
  correct_choice_ids?: string[];
  // short-answer
  starter_code?: string;
  // parsons
  options?: string[];
  required_block_count?: number;
  // dropdown
  blanks?: { id: string; options: string[]; correct: string }[];
  prompt_template?: string;
  // execution-trace
  function_name?: string;
  function_source?: string;
  call_expression?: string;
  checkpoints?: { id: string; label: string; options: string[]; correct: string }[];
}

export interface CodeModification {
  line_number: number;
  old_code: string;
  new_code: string;
  explanation?: string;
}

const TYPE_CONFIG: Record<string, { label: string; icon: typeof Bug; color: string; bg: string; border: string; desc: string }> = {
  "buggy-code": { 
    label: "Find the Bug", 
    icon: Bug, 
    color: "text-red-700", 
    bg: "bg-red-50", 
    border: "border-red-200",
    desc: "Identify and explain the error"
  },
  "output-prediction": { 
    label: "Predict Output", 
    icon: Eye, 
    color: "text-blue-700", 
    bg: "bg-blue-50", 
    border: "border-blue-200",
    desc: "What will this code print?"
  },
  "code-completion": { 
    label: "Complete Code", 
    icon: Code, 
    color: "text-purple-700", 
    bg: "bg-purple-50", 
    border: "border-purple-200",
    desc: "Fill in the missing parts"
  },
  "multiple-choice": { 
    label: "Concept Check", 
    icon: ListChecks, 
    color: "text-emerald-700", 
    bg: "bg-emerald-50", 
    border: "border-emerald-200",
    desc: "Test your understanding"
  },
  "short-answer": { 
    label: "Write Code", 
    icon: FileText, 
    color: "text-amber-700", 
    bg: "bg-amber-50", 
    border: "border-amber-200",
    desc: "Solve by writing code"
  },
  parsons: { 
    label: "Parsons Puzzle", 
    icon: Puzzle, 
    color: "text-orange-700", 
    bg: "bg-orange-50", 
    border: "border-orange-200",
    desc: "Reorder the code blocks"
  },
  dropdown: { 
    label: "Fill Blanks", 
    icon: Terminal, 
    color: "text-teal-700", 
    bg: "bg-teal-50", 
    border: "border-teal-200",
    desc: "Select the correct options"
  },
  "execution-trace": { 
    label: "Trace Code", 
    icon: Brain, 
    color: "text-indigo-700", 
    bg: "bg-indigo-50", 
    border: "border-indigo-200",
    desc: "Follow the execution flow"
  },
};

// Header component for problem types that don't have their own header
function ProblemTypeHeader({ problem }: { problem: TeachProblem }) {
  const config = TYPE_CONFIG[problem.problem_type] || { 
    label: problem.problem_type, 
    icon: FileText, 
    color: "text-stone-700", 
    bg: "bg-stone-50", 
    border: "border-stone-200",
    desc: ""
  };
  const Icon = config.icon;

  return (
    <div className={`px-4 py-3 border-b ${config.border} ${config.bg}`}>
      <div className="flex items-center gap-2 mb-1">
        <div className={`w-7 h-7 rounded-lg ${config.bg} ${config.border} border flex items-center justify-center`}>
          <Icon className={`w-4 h-4 ${config.color}`} />
        </div>
        <span className={`text-xs font-bold uppercase tracking-wider ${config.color}`}>
          {config.label}
        </span>
      </div>
      <p className="text-base text-stone-700 font-medium leading-relaxed">{problem.problem_statement}</p>
      {config.desc && (
        <p className="text-xs text-stone-500 mt-1">{config.desc}</p>
      )}
    </div>
  );
}

interface ProblemRendererProps {
  problem: TeachProblem;
  codeModifications?: CodeModification[];
  onStudentAnswer?: (answer: Record<string, unknown>) => void;
  disabled?: boolean;
  userId?: number;
  username?: string;
  onLineClick?: (lineNum: number, lineContent: string) => void;
}

export function ProblemRenderer({ problem, codeModifications, onStudentAnswer, disabled, userId, username, onLineClick }: ProblemRendererProps) {
  const t = problem.problem_type;

  if (t === "buggy-code" && problem.code) {
    return (
      <BuggyCodeBlock
        code={problem.code}
        bugLines={problem.bug_lines ?? []}
        modifications={codeModifications ?? []}
        problemStatement={problem.problem_statement}
        userId={userId}
        username={username}
        onLineClick={onLineClick}
      />
    );
  }

  if (t === "output-prediction" && problem.code) {
    return (
      <OutputPrediction
        code={problem.code}
        problemStatement={problem.problem_statement}
        onAnswer={(v) => onStudentAnswer?.({ predicted_output: v })}
        disabled={disabled}
      />
    );
  }

  if (t === "code-completion" && problem.code_template) {
    return (
      <CodeCompletion
        codeTemplate={problem.code_template}
        slots={problem.completion_slots ?? []}
        modifications={codeModifications ?? []}
        problemStatement={problem.problem_statement}
      />
    );
  }

  if (t === "multiple-choice" && problem.choices) {
    return (
      <div className="flex flex-col h-full">
        <ProblemTypeHeader problem={problem} />
        <div className="flex-1 overflow-auto p-4">
          <ConceptMCQ
            problemStatement="" // Empty because header shows it
            choices={problem.choices}
            onAnswer={(ids) => onStudentAnswer?.({ selected_ids: ids })}
            disabled={disabled}
          />
        </div>
      </div>
    );
  }

  if (t === "short-answer") {
    return (
      <div className="flex flex-col h-full">
        <ProblemTypeHeader problem={problem} />
        <div className="flex-1 p-4">
          <ShortCodeAnswer
            problemStatement="" // Empty because header shows it
            starterCode={problem.starter_code ?? ""}
            onAnswer={(code) => onStudentAnswer?.({ code })}
            disabled={disabled}
          />
        </div>
      </div>
    );
  }

  if (t === "parsons" && problem.options) {
    return (
      <div className="flex flex-col h-full">
        <ProblemTypeHeader problem={problem} />
        <div className="flex-1 overflow-auto p-4">
          <ParsonsBlock
            options={problem.options}
            requiredBlockCount={problem.required_block_count ?? 0}
            selectedBlocks={[]}
            onSelectedChange={(blocks) => onStudentAnswer?.({ selected_blocks: blocks })}
            disabled={disabled}
          />
        </div>
      </div>
    );
  }

  if (t === "dropdown" && problem.blanks) {
    const mappedBlanks = problem.blanks.map((b) => ({
      blank_id: b.id,
      placeholder: b.id,
      options: b.options,
    }));
    return (
      <div className="flex flex-col h-full">
        <ProblemTypeHeader problem={problem} />
        <div className="flex-1 overflow-auto p-4">
          <DropdownBlanks
            promptTemplate={problem.prompt_template ?? ""}
            blanks={mappedBlanks}
            selectedAnswers={{}}
            onAnswerChange={(id, val) => onStudentAnswer?.({ [`blank_${id}`]: val })}
            disabled={disabled}
          />
        </div>
      </div>
    );
  }

  if (t === "execution-trace" && problem.checkpoints) {
    const mappedCheckpoints = problem.checkpoints.map((c) => ({
      checkpoint_id: c.id,
      line_number: 0,
      line_excerpt: c.label,
      variable_name: c.label,
      options: c.options,
    }));
    return (
      <div className="flex flex-col h-full">
        <ProblemTypeHeader problem={problem} />
        <div className="flex-1 overflow-auto p-4">
          <ExecutionTrace
            functionName={problem.function_name ?? ""}
            functionSource={problem.function_source ?? ""}
            callExpression={problem.call_expression ?? ""}
            checkpoints={mappedCheckpoints}
            selectedAnswers={{}}
            onAnswerChange={(id, val) => onStudentAnswer?.({ [`checkpoint_${id}`]: val })}
            disabled={disabled}
          />
        </div>
      </div>
    );
  }

  // Fallback: simple code display with header
  return (
    <div className="flex flex-col h-full">
      <ProblemTypeHeader problem={problem} />
      {problem.code && (
        <div className="flex-1 overflow-auto bg-[#1a1a2e] p-4">
          <pre className="text-sm font-mono text-stone-200 whitespace-pre-wrap select-none ocr-noise">
            {problem.code}
          </pre>
        </div>
      )}
    </div>
  );
}
