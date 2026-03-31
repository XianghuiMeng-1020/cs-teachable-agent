export type TaskSummary = {
  queryId: string;
  taskId: string;
  taskIndex: number;
  totalNumTc: number | null;
  genConsistency: number | null;
  llmJudge: number | null;
  qTestsuite: number | null;
  qContext: number | null;
  totalNumStu: number | null;
  numPassedStu: number | null;
  studentPassRate: number | null;
  pyTaskSyn50Passed: boolean;
  hasParsons: boolean;
  parsonsTitle: string | null;
  parsonsEvalPassRate: number | null;
  parsonsPopulationPassed: boolean | null;
};

export type QuerySummary = {
  queryId: string;
  queryIndex: number;
  taskCount: number;
  typedItemCount: number;
  pyTaskSyn50Count: number;
  averageStudentPassRate: number | null;
  tasks: TaskSummary[];
};

export type ParsonsItemDetail = {
  itemId: string;
  itemType: string;
  title: string;
  prompt: string;
  gradingRule: string;
  functionName: string | null;
  codeBlocks: string[];
  solutionOrder: number[];
  distractors: string[];
  validationPassed: boolean | null;
  validationIssues: string[];
  metadataTheme: string | null;
  metadataConcepts: string[];
  qualityMetrics: Record<string, string>;
  filePath: string;
  markdownPath: string | null;
};

export type TypedAssessmentEvalSummary = {
  itemId: string;
  itemType: string;
  model: string;
  temperature: number;
  numStudents: number;
  numPassed: number;
  passRate: number;
  populationPassThreshold: number;
  populationPassed: boolean;
  outputDir: string;
};

export type TaskDetail = {
  queryId: string;
  taskId: string;
  sourceTaskPath: string;
  taskDescription: string | null;
  solutionProgram: string | null;
  testSuite: string | null;
  summary: TaskSummary | null;
  typedItem: ParsonsItemDetail | null;
  typedEval: TypedAssessmentEvalSummary | null;
};

export type StudioIndexResponse = {
  queries: QuerySummary[];
};

export type StudioTaskResponse = TaskDetail;

export type StudentTaskListItem = {
  queryId: string;
  taskId: string;
  itemId: string;
  itemType: "parsons" | "dropdown" | "execution-trace";
  title: string;
  theme: string | null;
  aiPassRate: number | null;
  studentPassRate: number | null;
};

export type StudentDropdownBlank = {
  blankId: string;
  placeholder: string;
  options: string[];
};

export type StudentExecutionTraceCheckpoint = {
  checkpointId: string;
  lineNumber: number;
  lineExcerpt: string;
  variableName: string;
};

type StudentTaskBase = {
  queryId: string;
  taskId: string;
  itemId: string;
  itemType: "parsons" | "dropdown" | "execution-trace";
  title: string;
  prompt: string;
  theme: string | null;
  concepts: string[];
  aiPassRate: number | null;
};

export type StudentParsonsTaskResponse = StudentTaskBase & {
  itemType: "parsons";
  requiredBlockCount: number;
  options: string[];
};

export type StudentDropdownTaskResponse = StudentTaskBase & {
  itemType: "dropdown";
  requiredBlankCount: number;
  promptTemplate: string;
  blanks: StudentDropdownBlank[];
};

export type StudentExecutionTraceTaskResponse = StudentTaskBase & {
  itemType: "execution-trace";
  requiredCheckpointCount: number;
  functionName: string;
  functionSource: string;
  callExpression: string;
  checkpoints: StudentExecutionTraceCheckpoint[];
};

export type StudentTaskResponse =
  | StudentParsonsTaskResponse
  | StudentDropdownTaskResponse
  | StudentExecutionTraceTaskResponse;

type StudentGradeBase = {
  itemType: "parsons" | "dropdown" | "execution-trace";
  correct: boolean;
  feedback: string;
  expectedCount: number;
  selectedCount: number;
  correctCount: number;
};

export type StudentParsonsGradeResponse = StudentGradeBase & {
  itemType: "parsons";
};

export type StudentDropdownGradeResponse = StudentGradeBase & {
  itemType: "dropdown";
};

export type StudentExecutionTraceGradeResponse = StudentGradeBase & {
  itemType: "execution-trace";
};

export type StudentGradeResponse =
  | StudentParsonsGradeResponse
  | StudentDropdownGradeResponse
  | StudentExecutionTraceGradeResponse;

export type StudentHintType = "understand" | "next-step" | "check-one-issue";

export type StudentHintLevel = 1 | 2 | 3;

export type StudentHintTarget = {
  kind: "blank" | "checkpoint" | "block" | "task";
  id: string;
  label: string;
} | null;

export type StudentHintRequest = {
  queryId: string;
  taskId: string;
  itemType: "parsons" | "dropdown" | "execution-trace";
  hintType: StudentHintType;
  level: StudentHintLevel;
  taskContext?: StudentTaskResponse;
  reflection?: string;
  progressSummary?: string | null;
  attemptNumber?: number | null;
  lastFeedback?: StudentGradeResponse | null;
  selectedBlocks?: string[];
  selectedAnswers?: Record<string, string>;
};

export type StudentHintResponse = {
  hintId: string;
  hintType: StudentHintType;
  level: StudentHintLevel;
  title: string;
  body: string;
  target: StudentHintTarget;
  escalationAvailable: boolean;
  model: string;
};

export type StudentTelemetryEventType =
  | "session_started"
  | "session_ended"
  | "task_loaded"
  | "attempt_started"
  | "attempt_reset"
  | "submit_clicked"
  | "graded_correct"
  | "graded_incorrect"
  | "focus_lost"
  | "resume_clicked"
  | "block_added"
  | "block_removed"
  | "block_reordered"
  | "pool_shuffled"
  | "blank_selected"
  | "blank_changed"
  | "checkpoint_blurred"
  | "hint_requested"
  | "hint_received"
  | "hint_request_failed"
  | "hint_helpful"
  | "hint_unhelpful"
  | "hint_stronger_requested"
  | "hint_escalation_saved";

export type StudentTelemetryEvent = {
  eventId: string;
  sessionId: string;
  attemptId?: string | null;
  attemptNumber?: number | null;
  queryId?: string | null;
  taskId?: string | null;
  itemId?: string | null;
  itemType?: "parsons" | "dropdown" | "execution-trace" | null;
  eventType: StudentTelemetryEventType;
  eventTime: string;
  payload: Record<string, unknown>;
};

export type StudentAttemptRecord = {
  attemptId: string;
  sessionId: string;
  attemptNumber: number;
  queryId: string;
  taskId: string;
  itemId: string;
  itemType: "parsons" | "dropdown" | "execution-trace";
  startedAt: string;
  submittedAt: string;
  durationMs: number;
  focusLossCount: number;
  isCorrect: boolean;
  score: number;
  expectedCount: number;
  selectedCount: number;
  correctCount: number;
  submission: Record<string, unknown>;
  feedback: StudentGradeResponse;
};
