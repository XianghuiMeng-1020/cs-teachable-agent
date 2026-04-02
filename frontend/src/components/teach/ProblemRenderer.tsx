import { BuggyCodeBlock } from "./BuggyCodeBlock";
import { OutputPrediction } from "./OutputPrediction";
import { CodeCompletion } from "./CodeCompletion";
import { ConceptMCQ } from "./ConceptMCQ";
import { ShortCodeAnswer } from "./ShortCodeAnswer";
import { ParsonsBlock } from "@/components/assessment/ParsonsBlock";
import { DropdownBlanks } from "@/components/assessment/DropdownBlanks";
import { ExecutionTrace } from "@/components/assessment/ExecutionTrace";

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
      <ConceptMCQ
        problemStatement={problem.problem_statement}
        choices={problem.choices}
        onAnswer={(ids) => onStudentAnswer?.({ selected_ids: ids })}
        disabled={disabled}
      />
    );
  }

  if (t === "short-answer") {
    return (
      <ShortCodeAnswer
        problemStatement={problem.problem_statement}
        starterCode={problem.starter_code ?? ""}
        onAnswer={(code) => onStudentAnswer?.({ code })}
        disabled={disabled}
      />
    );
  }

  if (t === "parsons" && problem.options) {
    return (
      <div className="space-y-3">
        <p className="text-sm text-stone-700 whitespace-pre-wrap">{problem.problem_statement}</p>
        <ParsonsBlock
          options={problem.options}
          requiredBlockCount={problem.required_block_count ?? 0}
          selectedBlocks={[]}
          onSelectedChange={(blocks) => onStudentAnswer?.({ selected_blocks: blocks })}
          disabled={disabled}
        />
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
      <div className="space-y-3">
        <p className="text-sm text-stone-700 whitespace-pre-wrap">{problem.problem_statement}</p>
        <DropdownBlanks
          promptTemplate={problem.prompt_template ?? ""}
          blanks={mappedBlanks}
          selectedAnswers={{}}
          onAnswerChange={(id, val) => onStudentAnswer?.({ [`blank_${id}`]: val })}
          disabled={disabled}
        />
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
      <div className="space-y-3">
        <p className="text-sm text-stone-700 whitespace-pre-wrap">{problem.problem_statement}</p>
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
    );
  }

  // Fallback: simple code display
  return (
    <div className="space-y-3">
      <p className="text-sm text-stone-700 whitespace-pre-wrap">{problem.problem_statement}</p>
      {problem.code && (
        <pre className="bg-stone-900 text-stone-100 p-4 rounded-lg text-sm overflow-x-auto font-mono select-none ocr-noise">
          {problem.code}
        </pre>
      )}
    </div>
  );
}
