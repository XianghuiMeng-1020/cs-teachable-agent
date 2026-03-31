import { existsSync } from "node:fs";
import { readdir, readFile } from "node:fs/promises";
import path from "node:path";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import type {
  ParsonsItemDetail,
  QuerySummary,
  StudentGradeResponse,
  StudentTaskListItem,
  StudentTaskResponse,
  StudioIndexResponse,
  TaskDetail,
  TaskSummary,
  TypedAssessmentEvalSummary
} from "@/src/types";

const execFileAsync = promisify(execFile);
type StudentSupportedItemType = "parsons" | "dropdown" | "execution-trace";
type LoadStudentDataOptions = {
  bypassCache?: boolean;
};

type StudentTaskRecord = {
  queryId: string;
  taskId: string;
  itemId: string;
  itemType: StudentSupportedItemType;
  title: string;
  prompt: string;
  theme: string | null;
  concepts: string[];
  aiPassRate: number | null;
  interaction: Record<string, unknown>;
};

const STUDENT_TASK_CACHE_TTL_MS = process.env.NODE_ENV === "production" ? 5 * 60_000 : 15_000;
const studentTaskRecordCache = new Map<string, { expiresAt: number; value: StudentTaskRecord }>();

function isNoise(name: string): boolean {
  return name.startsWith("._") || name === "__pycache__";
}

function sortByNumericSuffix<T extends string>(values: T[]): T[] {
  return [...values].sort((left, right) => {
    const leftIndex = Number.parseInt(left.split("_").at(-1) ?? "0", 10);
    const rightIndex = Number.parseInt(right.split("_").at(-1) ?? "0", 10);
    return leftIndex - rightIndex;
  });
}

function resolveRepoRoot(): string {
  const cwd = process.cwd();
  const directOutputs = path.join(cwd, "outputs");
  const parentOutputs = path.join(cwd, "..", "outputs");

  if (existsSync(directOutputs)) {
    return cwd;
  }

  if (existsSync(parentOutputs)) {
    return path.resolve(cwd, "..");
  }

  throw new Error("Could not locate repo root with outputs/ directory.");
}

function parseCsvLine(line: string): string[] {
  const cells: string[] = [];
  let current = "";
  let inQuotes = false;

  for (let index = 0; index < line.length; index += 1) {
    const char = line[index];
    const next = line[index + 1];

    if (char === '"') {
      if (inQuotes && next === '"') {
        current += '"';
        index += 1;
      } else {
        inQuotes = !inQuotes;
      }
      continue;
    }

    if (char === "," && !inQuotes) {
      cells.push(current);
      current = "";
      continue;
    }

    current += char;
  }

  cells.push(current);
  return cells;
}

function parseCsv(text: string): Array<Record<string, string>> {
  const lines = text
    .split(/\r?\n/)
    .map((line) => line.trimEnd())
    .filter((line) => line.length > 0);

  if (lines.length === 0) {
    return [];
  }

  const header = parseCsvLine(lines[0]);
  return lines.slice(1).map((line) => {
    const values = parseCsvLine(line);
    return header.reduce<Record<string, string>>((record, key, index) => {
      record[key] = values[index] ?? "";
      return record;
    }, {});
  });
}

function toNumber(value: string | undefined): number | null {
  if (!value) {
    return null;
  }
  const parsed = Number.parseFloat(value);
  return Number.isFinite(parsed) ? parsed : null;
}

function toBoolean(value: unknown): boolean | null {
  if (typeof value === "boolean") {
    return value;
  }
  return null;
}

function normalizeBlock(text: string): string {
  return text.replace(/\r\n/g, "\n").trim();
}

async function readFileIfExists(filePath: string): Promise<string | null> {
  try {
    return await readFile(filePath, "utf8");
  } catch {
    return null;
  }
}

async function readJsonIfExists<T>(filePath: string): Promise<T | null> {
  const text = await readFileIfExists(filePath);
  if (!text) {
    return null;
  }
  return JSON.parse(text) as T;
}

async function listTaskDirs(queryDir: string): Promise<string[]> {
  const entries = await readdir(queryDir, { withFileTypes: true });
  return sortByNumericSuffix(
    entries
      .filter((entry) => entry.isDirectory() && /^task_\d+$/.test(entry.name) && !isNoise(entry.name))
      .map((entry) => entry.name)
  );
}

async function findParsonsJson(taskDir: string, taskId: string): Promise<string | null> {
  const preferred = path.join(taskDir, `${taskId}-parsons.json`);
  if (existsSync(preferred)) {
    return preferred;
  }

  const entries = await readdir(taskDir, { withFileTypes: true });
  const match = entries.find(
    (entry) => entry.isFile() && entry.name.endsWith("-parsons.json") && !isNoise(entry.name)
  );
  return match ? path.join(taskDir, match.name) : null;
}

async function loadParsonsDetail(taskDir: string, taskId: string): Promise<ParsonsItemDetail | null> {
  const jsonPath = await findParsonsJson(taskDir, taskId);
  if (!jsonPath) {
    return null;
  }

  const raw = await readJsonIfExists<Record<string, unknown>>(jsonPath);
  if (!raw) {
    return null;
  }

  const interactionContent = (raw.interaction_content ?? {}) as Record<string, unknown>;
  const metadata = (raw.metadata ?? {}) as Record<string, unknown>;
  const validation = (raw.validation ?? {}) as Record<string, unknown>;
  const qualityMetrics = (metadata.quality_metrics ?? {}) as Record<string, unknown>;
  const markdownPath = jsonPath.replace(/\.json$/, ".md");

  return {
    itemId: String(raw.item_id ?? taskId),
    itemType: String(raw.item_type ?? "parsons"),
    title: String(raw.title ?? taskId),
    prompt: String(raw.prompt ?? ""),
    gradingRule: String(raw.grading_rule ?? ""),
    functionName: typeof interactionContent.function_name === "string" ? interactionContent.function_name : null,
    codeBlocks: Array.isArray(interactionContent.code_blocks)
      ? interactionContent.code_blocks.map((block) => String(block))
      : [],
    solutionOrder: Array.isArray(interactionContent.solution_order)
      ? interactionContent.solution_order.map((value) => Number(value))
      : [],
    distractors: Array.isArray(interactionContent.distractors)
      ? interactionContent.distractors.map((block) => String(block))
      : [],
    validationPassed: toBoolean(validation.passed),
    validationIssues: Array.isArray(validation.issues)
      ? validation.issues.map((issue) => String((issue as { message?: unknown }).message ?? issue))
      : [],
    metadataTheme: typeof metadata.theme === "string" ? metadata.theme : null,
    metadataConcepts: Array.isArray(metadata.concepts)
      ? metadata.concepts.map((concept) => String(concept))
      : [],
    qualityMetrics: Object.fromEntries(
      Object.entries(qualityMetrics).map(([key, value]) => [key, String(value)])
    ),
    filePath: jsonPath,
    markdownPath: existsSync(markdownPath) ? markdownPath : null
  };
}

function getCanonicalOrderedBlocks(item: ParsonsItemDetail): string[] {
  return item.solutionOrder.map((index) => item.codeBlocks[index]).filter((block): block is string => typeof block === "string");
}

async function loadParsonsEval(taskDir: string, taskId: string): Promise<TypedAssessmentEvalSummary | null> {
  const jsonPath = await findParsonsJson(taskDir, taskId);
  if (!jsonPath) {
    return null;
  }

  const baseName = path.basename(jsonPath, ".json");
  const summaryPath = path.join(taskDir, `${baseName}-eval`, "summary.json");
  const raw = await readJsonIfExists<Record<string, unknown>>(summaryPath);
  if (!raw) {
    return null;
  }

  return {
    itemId: String(raw.item_id ?? baseName),
    itemType: String(raw.item_type ?? "parsons"),
    model: String(raw.model ?? "unknown"),
    temperature: Number(raw.temperature ?? 0),
    numStudents: Number(raw.num_students ?? 0),
    numPassed: Number(raw.num_passed ?? 0),
    passRate: Number(raw.pass_rate ?? 0),
    populationPassThreshold: Number(raw.population_pass_threshold ?? 0),
    populationPassed: Boolean(raw.population_passed),
    outputDir: String(raw.output_dir ?? path.dirname(summaryPath))
  };
}

function parseStudentItemType(fileName: string): StudentSupportedItemType | null {
  if (fileName.endsWith("-parsons.json")) {
    return "parsons";
  }
  if (fileName.endsWith("-dropdown.json")) {
    return "dropdown";
  }
  if (fileName.endsWith("-execution-trace.json")) {
    return "execution-trace";
  }
  return null;
}

async function findTypedAssessmentJson(
  taskDir: string,
  taskId: string,
  itemType: StudentSupportedItemType
): Promise<string | null> {
  const preferred = path.join(taskDir, `${taskId}-${itemType}.json`);
  if (existsSync(preferred)) {
    return preferred;
  }

  const entries = await readdir(taskDir, { withFileTypes: true });
  const match = entries.find(
    (entry) => entry.isFile() && entry.name.endsWith(`-${itemType}.json`) && !isNoise(entry.name)
  );
  return match ? path.join(taskDir, match.name) : null;
}

async function listStudentTypedItemTypes(taskDir: string): Promise<StudentSupportedItemType[]> {
  const entries = await readdir(taskDir, { withFileTypes: true });
  const types = entries
    .filter((entry) => entry.isFile() && !isNoise(entry.name))
    .map((entry) => parseStudentItemType(entry.name))
    .filter((value): value is StudentSupportedItemType => value !== null);
  return [...new Set(types)];
}

async function loadTypedAssessmentEval(
  taskDir: string,
  taskId: string,
  itemType: StudentSupportedItemType
): Promise<TypedAssessmentEvalSummary | null> {
  const jsonPath = await findTypedAssessmentJson(taskDir, taskId, itemType);
  if (!jsonPath) {
    return null;
  }

  return loadTypedAssessmentEvalFromJsonPath(jsonPath, itemType);
}

async function loadTypedAssessmentEvalFromJsonPath(
  jsonPath: string,
  itemType: StudentSupportedItemType
): Promise<TypedAssessmentEvalSummary | null> {
  const baseName = path.basename(jsonPath, ".json");
  const summaryPath = path.join(path.dirname(jsonPath), `${baseName}-eval`, "summary.json");
  const raw = await readJsonIfExists<Record<string, unknown>>(summaryPath);
  if (!raw) {
    return null;
  }

  return {
    itemId: String(raw.item_id ?? baseName),
    itemType: String(raw.item_type ?? itemType),
    model: String(raw.model ?? "unknown"),
    temperature: Number(raw.temperature ?? 0),
    numStudents: Number(raw.num_students ?? 0),
    numPassed: Number(raw.num_passed ?? 0),
    passRate: Number(raw.pass_rate ?? 0),
    populationPassThreshold: Number(raw.population_pass_threshold ?? 0),
    populationPassed: Boolean(raw.population_passed),
    outputDir: String(raw.output_dir ?? path.dirname(summaryPath))
  };
}

async function readQueryStudentPassRates(queryDir: string): Promise<Map<string, number | null>> {
  const rates = new Map<string, number | null>();
  const resultsText = await readFileIfExists(path.join(queryDir, "results.csv"));
  if (!resultsText) {
    return rates;
  }

  for (const row of parseCsv(resultsText)) {
    const totalNumStu = toNumber(row.total_num_stu);
    const numPassedStu = toNumber(row.num_passed_stu);
    const studentPassRate =
      totalNumStu && totalNumStu > 0 && numPassedStu !== null ? (numPassedStu / totalNumStu) * 100 : null;
    if (row.task) {
      rates.set(row.task, studentPassRate);
    }
  }
  return rates;
}

function getStudentTaskRecordCacheKey(
  queryId: string,
  taskId: string,
  itemType: StudentSupportedItemType
): string {
  return `${queryId}::${taskId}::${itemType}`;
}

async function loadStudentTaskRecord(
  queryId: string,
  taskId: string,
  itemType: StudentSupportedItemType,
  options: LoadStudentDataOptions = {}
): Promise<StudentTaskRecord> {
  const cacheKey = getStudentTaskRecordCacheKey(queryId, taskId, itemType);
  const cached = studentTaskRecordCache.get(cacheKey);
  const now = Date.now();

  if (!options.bypassCache && cached && cached.expiresAt > now) {
    return cached.value;
  }

  const repoRoot = resolveRepoRoot();
  const taskDir = path.join(repoRoot, "outputs", queryId, taskId);
  const jsonPath = await findTypedAssessmentJson(taskDir, taskId, itemType);
  if (!jsonPath) {
    throw new Error(`No ${itemType} item found for ${queryId}/${taskId}.`);
  }

  const [raw, typedEval] = await Promise.all([
    readJsonIfExists<Record<string, unknown>>(jsonPath),
    loadTypedAssessmentEvalFromJsonPath(jsonPath, itemType)
  ]);

  if (!raw) {
    throw new Error(`Failed to read ${itemType} item for ${queryId}/${taskId}.`);
  }

  const interaction = (raw.interaction_content ?? {}) as Record<string, unknown>;
  const metadata = (raw.metadata ?? {}) as Record<string, unknown>;
  const value = {
    queryId,
    taskId,
    itemId: String(raw.item_id ?? `${taskId}-${itemType}`),
    itemType,
    title: String(raw.title ?? taskId),
    prompt: String(raw.prompt ?? ""),
    theme: typeof metadata.theme === "string" ? metadata.theme : null,
    concepts: Array.isArray(metadata.concepts) ? metadata.concepts.map((concept) => String(concept)) : [],
    aiPassRate: typedEval?.passRate ?? null,
    interaction
  } satisfies StudentTaskRecord;

  studentTaskRecordCache.set(cacheKey, {
    expiresAt: now + STUDENT_TASK_CACHE_TTL_MS,
    value
  });

  return value;
}

async function loadStudentTaskResponse(
  queryId: string,
  taskId: string,
  itemType: StudentSupportedItemType,
  options: LoadStudentDataOptions = {}
): Promise<StudentTaskResponse> {
  const record = await loadStudentTaskRecord(queryId, taskId, itemType, options);

  const base = {
    queryId,
    taskId,
    itemId: record.itemId,
    itemType,
    title: record.title,
    prompt: record.prompt,
    theme: record.theme,
    concepts: record.concepts,
    aiPassRate: record.aiPassRate
  } as const;

  if (itemType === "parsons") {
    const codeBlocks = Array.isArray(record.interaction.code_blocks)
      ? record.interaction.code_blocks.map((block) => String(block))
      : [];
    const distractors = Array.isArray(record.interaction.distractors)
      ? record.interaction.distractors.map((block) => String(block))
      : [];

    return {
      ...base,
      itemType: "parsons",
      requiredBlockCount: codeBlocks.length,
      options: [...codeBlocks, ...distractors]
    };
  }

  if (itemType === "execution-trace") {
    const checkpoints = Array.isArray(record.interaction.checkpoints)
      ? record.interaction.checkpoints.map((checkpoint) => {
          const rawCheckpoint = checkpoint as Record<string, unknown>;
          return {
            checkpointId: String(rawCheckpoint.checkpoint_id ?? ""),
            lineNumber: Number(rawCheckpoint.line_number ?? 0),
            lineExcerpt: String(rawCheckpoint.line_excerpt ?? ""),
            variableName: String(rawCheckpoint.variable_name ?? "")
          };
        })
      : [];

    return {
      ...base,
      itemType: "execution-trace",
      requiredCheckpointCount: checkpoints.length,
      functionName: String(record.interaction.function_name ?? ""),
      functionSource: String(record.interaction.function_source ?? ""),
      callExpression: String(record.interaction.call_expression ?? ""),
      checkpoints
    };
  }

  const blanks = Array.isArray(record.interaction.blanks)
    ? record.interaction.blanks.map((blank) => {
        const rawBlank = blank as Record<string, unknown>;
        return {
          blankId: String(rawBlank.blank_id ?? ""),
          placeholder: String(rawBlank.placeholder ?? ""),
          options: Array.isArray(rawBlank.options) ? rawBlank.options.map((option) => String(option)) : []
        };
      })
    : [];

  return {
    ...base,
    itemType: "dropdown",
    requiredBlankCount: blanks.length,
    promptTemplate: String(record.interaction.prompt_template ?? ""),
    blanks
  };
}

async function loadDropdownCorrectAnswers(
  queryId: string,
  taskId: string
): Promise<Map<string, string>> {
  const repoRoot = resolveRepoRoot();
  const taskDir = path.join(repoRoot, "outputs", queryId, taskId);
  const jsonPath = await findTypedAssessmentJson(taskDir, taskId, "dropdown");
  if (!jsonPath) {
    throw new Error(`No dropdown item found for ${queryId}/${taskId}.`);
  }

  const raw = await readJsonIfExists<Record<string, unknown>>(jsonPath);
  if (!raw) {
    throw new Error(`Failed to read dropdown item for ${queryId}/${taskId}.`);
  }

  const interaction = (raw.interaction_content ?? {}) as Record<string, unknown>;
  const blanks = Array.isArray(interaction.blanks) ? interaction.blanks : [];
  const answers = new Map<string, string>();

  for (const blank of blanks) {
    const rawBlank = blank as Record<string, unknown>;
    answers.set(String(rawBlank.blank_id ?? ""), String(rawBlank.correct_answer ?? ""));
  }

  return answers;
}

async function loadExecutionTraceCorrectAnswers(
  queryId: string,
  taskId: string
): Promise<Map<string, string>> {
  const repoRoot = resolveRepoRoot();
  const taskDir = path.join(repoRoot, "outputs", queryId, taskId);
  const jsonPath = await findTypedAssessmentJson(taskDir, taskId, "execution-trace");
  if (!jsonPath) {
    throw new Error(`No execution-trace item found for ${queryId}/${taskId}.`);
  }

  const raw = await readJsonIfExists<Record<string, unknown>>(jsonPath);
  if (!raw) {
    throw new Error(`Failed to read execution-trace item for ${queryId}/${taskId}.`);
  }

  const answerKey = (raw.answer_key ?? {}) as Record<string, unknown>;
  const correctAnswers = (answerKey.correct_answers ?? {}) as Record<string, unknown>;
  return new Map(Object.entries(correctAnswers).map(([key, value]) => [key, String(value)]));
}

async function buildTaskSummary(queryId: string, queryDir: string, row: Record<string, string>): Promise<TaskSummary> {
  const taskId = row.task;
  const taskDir = path.join(queryDir, taskId);
  const typedItem = await loadParsonsDetail(taskDir, taskId);
  const typedEval = await loadParsonsEval(taskDir, taskId);
  const totalNumStu = toNumber(row.total_num_stu);
  const numPassedStu = toNumber(row.num_passed_stu);
  const studentPassRate =
    totalNumStu && totalNumStu > 0 && numPassedStu !== null ? (numPassedStu / totalNumStu) * 100 : null;
  const genConsistency = toNumber(row.gen_consistency);
  const qTestsuite = toNumber(row["Q-Testsuite"]);
  const qContext = toNumber(row["Q-Context"]);
  const pyTaskSyn50Passed =
    genConsistency === 1 && qTestsuite === 1 && qContext === 1 && (studentPassRate ?? 0) >= 50;

  return {
    queryId,
    taskId,
    taskIndex: Number.parseInt(taskId.split("_")[1] ?? "0", 10),
    totalNumTc: toNumber(row.total_num_tc),
    genConsistency,
    llmJudge: toNumber(row.LLMJudge),
    qTestsuite,
    qContext,
    totalNumStu,
    numPassedStu,
    studentPassRate,
    pyTaskSyn50Passed,
    hasParsons: typedItem !== null,
    parsonsTitle: typedItem?.title ?? null,
    parsonsEvalPassRate: typedEval?.passRate ?? null,
    parsonsPopulationPassed: typedEval?.populationPassed ?? null
  };
}

async function loadQuerySummary(queryId: string): Promise<QuerySummary> {
  const repoRoot = resolveRepoRoot();
  const queryDir = path.join(repoRoot, "outputs", queryId);
  const resultsPath = path.join(queryDir, "results.csv");
  const resultsText = await readFileIfExists(resultsPath);
  const rows = resultsText ? parseCsv(resultsText) : [];

  let tasks: TaskSummary[] = [];
  if (rows.length > 0) {
    tasks = await Promise.all(rows.map((row) => buildTaskSummary(queryId, queryDir, row)));
  } else {
    const taskDirs = await listTaskDirs(queryDir);
    tasks = await Promise.all(
      taskDirs.map(async (taskId) => {
        const taskDir = path.join(queryDir, taskId);
        const typedItem = await loadParsonsDetail(taskDir, taskId);
        const typedEval = await loadParsonsEval(taskDir, taskId);
        return {
          queryId,
          taskId,
          taskIndex: Number.parseInt(taskId.split("_")[1] ?? "0", 10),
          totalNumTc: null,
          genConsistency: null,
          llmJudge: null,
          qTestsuite: null,
          qContext: null,
          totalNumStu: null,
          numPassedStu: null,
          studentPassRate: null,
          pyTaskSyn50Passed: false,
          hasParsons: typedItem !== null,
          parsonsTitle: typedItem?.title ?? null,
          parsonsEvalPassRate: typedEval?.passRate ?? null,
          parsonsPopulationPassed: typedEval?.populationPassed ?? null
        } satisfies TaskSummary;
      })
    );
  }

  const typedItemCount = tasks.filter((task) => task.hasParsons).length;
  const pyTaskSyn50Count = tasks.filter((task) => task.pyTaskSyn50Passed).length;
  const studentRates = tasks
    .map((task) => task.studentPassRate)
    .filter((value): value is number => value !== null);
  const averageStudentPassRate =
    studentRates.length > 0
      ? Number((studentRates.reduce((sum, value) => sum + value, 0) / studentRates.length).toFixed(1))
      : null;

  return {
    queryId,
    queryIndex: Number.parseInt(queryId.split("_")[1] ?? "0", 10),
    taskCount: tasks.length,
    typedItemCount,
    pyTaskSyn50Count,
    averageStudentPassRate,
    tasks: tasks.sort((left, right) => left.taskIndex - right.taskIndex)
  };
}

export async function getStudioIndexData(): Promise<StudioIndexResponse> {
  const repoRoot = resolveRepoRoot();
  const outputsDir = path.join(repoRoot, "outputs");
  const entries = await readdir(outputsDir, { withFileTypes: true });
  const queryIds = sortByNumericSuffix(
    entries
      .filter((entry) => entry.isDirectory() && /^query_\d+$/.test(entry.name) && !isNoise(entry.name))
      .map((entry) => entry.name)
  );

  const queries = await Promise.all(queryIds.map((queryId) => loadQuerySummary(queryId)));
  return { queries };
}

export async function getTaskDetail(queryId: string, taskId: string): Promise<TaskDetail> {
  const repoRoot = resolveRepoRoot();
  const queryDir = path.join(repoRoot, "outputs", queryId);
  const taskDir = path.join(queryDir, taskId);
  const querySummary = await loadQuerySummary(queryId);
  const summary = querySummary.tasks.find((task) => task.taskId === taskId) ?? null;
  const typedItem = await loadParsonsDetail(taskDir, taskId);
  const typedEval = await loadParsonsEval(taskDir, taskId);

  return {
    queryId,
    taskId,
    sourceTaskPath: taskDir,
    taskDescription: await readFileIfExists(path.join(taskDir, "task_description.txt")),
    solutionProgram: await readFileIfExists(path.join(taskDir, "solution_program.py")),
    testSuite: await readFileIfExists(path.join(taskDir, "test_suite.py")),
    summary,
    typedItem,
    typedEval
  };
}

export async function getStudentEligibleTasks(
  maxAiPassRate: number,
  options: LoadStudentDataOptions = {}
): Promise<StudentTaskListItem[]> {
  const repoRoot = resolveRepoRoot();
  const outputsDir = path.join(repoRoot, "outputs");
  const entries = await readdir(outputsDir, { withFileTypes: true });
  const queryIds = sortByNumericSuffix(
    entries
      .filter((entry) => entry.isDirectory() && /^query_\d+$/.test(entry.name) && !isNoise(entry.name))
      .map((entry) => entry.name)
  );

  const perQueryItems = await Promise.all(
    queryIds.map(async (queryId) => {
      const queryDir = path.join(outputsDir, queryId);
      const studentRates = await readQueryStudentPassRates(queryDir);
      const taskDirs = await listTaskDirs(queryDir);

      const perTaskItems = await Promise.all(
        taskDirs.map(async (taskId) => {
          const taskDir = path.join(queryDir, taskId);
          const itemTypes = await listStudentTypedItemTypes(taskDir);
          const maybeItems = await Promise.all(
            itemTypes.map(async (itemType) => {
              const task = await loadStudentTaskRecord(queryId, taskId, itemType, options);
              if (task.aiPassRate === null || task.aiPassRate > maxAiPassRate) {
                return null;
              }
              return {
                queryId,
                taskId,
                itemId: task.itemId,
                itemType,
                title: task.title,
                theme: task.theme,
                aiPassRate: task.aiPassRate,
                studentPassRate: studentRates.get(taskId) ?? null
              } satisfies StudentTaskListItem;
            })
          );

          return maybeItems.flatMap((item) => (item ? [item] : []));
        })
      );

      return perTaskItems.flat();
    })
  );

  const items = perQueryItems.flat();

  return items.sort((left, right) => {
    const leftRate = left.aiPassRate ?? 101;
    const rightRate = right.aiPassRate ?? 101;
    if (leftRate !== rightRate) {
      return leftRate - rightRate;
    }
    if (left.queryId !== right.queryId) {
      return left.queryId.localeCompare(right.queryId, undefined, { numeric: true });
    }
    if (left.taskId !== right.taskId) {
      return left.taskId.localeCompare(right.taskId, undefined, { numeric: true });
    }
    return left.itemType.localeCompare(right.itemType);
  });
}

export async function getStudentTask(
  queryId: string,
  taskId: string,
  itemType: StudentSupportedItemType = "parsons",
  options: LoadStudentDataOptions = {}
): Promise<StudentTaskResponse> {
  return loadStudentTaskResponse(queryId, taskId, itemType, options);
}

export async function getStudentEligibleTaskPayload(
  maxAiPassRate: number,
  options: LoadStudentDataOptions = {}
): Promise<{ items: StudentTaskListItem[]; initialTask: StudentTaskResponse | null }> {
  const items = await getStudentEligibleTasks(maxAiPassRate, options);
  const firstItem = items[0];

  if (!firstItem) {
    return {
      items,
      initialTask: null
    };
  }

  return {
    items,
    initialTask: await loadStudentTaskResponse(firstItem.queryId, firstItem.taskId, firstItem.itemType, options)
  };
}

export async function gradeStudentTask(params: {
  queryId: string;
  taskId: string;
  itemType: StudentSupportedItemType;
  selectedBlocks?: string[];
  selectedAnswers?: Record<string, string>;
}): Promise<StudentGradeResponse> {
  const task = await loadStudentTaskResponse(params.queryId, params.taskId, params.itemType);

  if (task.itemType === "parsons") {
    const detail = await getTaskDetail(params.queryId, params.taskId);
    if (!detail.typedItem) {
      throw new Error(`No parsons item found for ${params.queryId}/${params.taskId}.`);
    }

    const canonicalBlocks = getCanonicalOrderedBlocks(detail.typedItem).map(normalizeBlock);
    const submittedBlocks = (params.selectedBlocks ?? []).map(normalizeBlock);
    const expectedCount = canonicalBlocks.length;
    const selectedCount = submittedBlocks.length;
    const correctCount = canonicalBlocks.reduce((count, block, index) => {
      return count + (submittedBlocks[index] === block ? 1 : 0);
    }, 0);

    const sameSet =
      selectedCount === expectedCount &&
      canonicalBlocks.every((block) => submittedBlocks.includes(block)) &&
      submittedBlocks.every((block) => canonicalBlocks.includes(block));
    const correct =
      selectedCount === expectedCount &&
      canonicalBlocks.every((block, index) => submittedBlocks[index] === block);

    if (correct) {
      return {
        itemType: "parsons",
        correct: true,
        feedback: "Correct. You selected the right blocks in the right order.",
        expectedCount,
        selectedCount,
        correctCount
      };
    }

    if (selectedCount !== expectedCount) {
      return {
        itemType: "parsons",
        correct: false,
        feedback: `Select exactly ${expectedCount} blocks before submitting.`,
        expectedCount,
        selectedCount,
        correctCount
      };
    }

    if (sameSet) {
      return {
        itemType: "parsons",
        correct: false,
        feedback: "You selected the right blocks, but the order is wrong.",
        expectedCount,
        selectedCount,
        correctCount
      };
    }

    return {
      itemType: "parsons",
      correct: false,
      feedback: "At least one selected block is a distractor or a required block is missing.",
      expectedCount,
      selectedCount,
      correctCount
    };
  }

  if (task.itemType === "execution-trace") {
    const submittedAnswers = params.selectedAnswers ?? {};
    const correctAnswers = await loadExecutionTraceCorrectAnswers(params.queryId, params.taskId);
    const checkpointIds = new Set(task.checkpoints.map((checkpoint) => checkpoint.checkpointId));
    const answeredCheckpoints = task.checkpoints.filter((checkpoint) => {
      const value = submittedAnswers[checkpoint.checkpointId];
      return typeof value === "string" && value.trim().length > 0;
    });
    const correctCount = task.checkpoints.reduce((count, checkpoint) => {
      return count + (submittedAnswers[checkpoint.checkpointId] === correctAnswers.get(checkpoint.checkpointId) ? 1 : 0);
    }, 0);
    const hasUnknownKeys = Object.keys(submittedAnswers).some((key) => !checkpointIds.has(key));
    const expectedCount = task.requiredCheckpointCount;
    const selectedCount = answeredCheckpoints.length;
    const correct = !hasUnknownKeys && correctCount === expectedCount && selectedCount === expectedCount;

    if (correct) {
      return {
        itemType: "execution-trace",
        correct: true,
        feedback: "Correct. Every checkpoint matches the canonical execution trace.",
        expectedCount,
        selectedCount,
        correctCount
      };
    }

    if (selectedCount !== expectedCount) {
      return {
        itemType: "execution-trace",
        correct: false,
        feedback: "Fill in every checkpoint value before submitting.",
        expectedCount,
        selectedCount,
        correctCount
      };
    }

    if (hasUnknownKeys) {
      return {
        itemType: "execution-trace",
        correct: false,
        feedback: "One or more values were attached to an unknown checkpoint. Review the checkpoint labels and try again.",
        expectedCount,
        selectedCount,
        correctCount
      };
    }

    if (correctCount > 0) {
      return {
        itemType: "execution-trace",
        correct: false,
        feedback: "Some checkpoint values are correct, but at least one traced value still differs from the canonical execution.",
        expectedCount,
        selectedCount,
        correctCount
      };
    }

    return {
      itemType: "execution-trace",
      correct: false,
      feedback: "None of the submitted checkpoint values match the canonical execution trace yet.",
      expectedCount,
      selectedCount,
      correctCount
    };
  }

  const submittedAnswers = params.selectedAnswers ?? {};
  const correctAnswers = await loadDropdownCorrectAnswers(params.queryId, params.taskId);
  const blankIds = new Set(task.blanks.map((blank) => blank.blankId));
  const answeredBlanks = task.blanks.filter((blank) => {
    const value = submittedAnswers[blank.blankId];
    return typeof value === "string" && value.trim().length > 0;
  });
  const correctCount = task.blanks.reduce((count, blank) => {
    return count + (submittedAnswers[blank.blankId] === correctAnswers.get(blank.blankId) ? 1 : 0);
  }, 0);
  const hasUnknownKeys = Object.keys(submittedAnswers).some((key) => !blankIds.has(key));
  const expectedCount = task.requiredBlankCount;
  const selectedCount = answeredBlanks.length;
  const correct = !hasUnknownKeys && correctCount === expectedCount && selectedCount === expectedCount;

  if (correct) {
    return {
      itemType: "dropdown",
      correct: true,
      feedback: "Correct. Every blank matches the canonical source solution.",
      expectedCount,
      selectedCount,
      correctCount
    };
  }

  if (selectedCount !== expectedCount) {
    return {
      itemType: "dropdown",
      correct: false,
      feedback: "Answer every blank before submitting.",
      expectedCount,
      selectedCount,
      correctCount
    };
  }

  if (hasUnknownKeys) {
    return {
      itemType: "dropdown",
      correct: false,
      feedback: "One or more answers were attached to an unknown blank. Review the blank labels and try again.",
      expectedCount,
      selectedCount,
      correctCount
    };
  }

  if (correctCount > 0) {
    return {
      itemType: "dropdown",
      correct: false,
      feedback: "Some blanks are correct, but at least one selected option still conflicts with the source solution.",
      expectedCount,
      selectedCount,
      correctCount
    };
  }

  return {
    itemType: "dropdown",
    correct: false,
    feedback: "None of the selected options match the canonical source solution yet.",
    expectedCount,
    selectedCount,
    correctCount
  };
}

export async function evaluateTypedAssessment(params: {
  queryId: string;
  taskId: string;
  model?: string;
  temperature?: number;
  numStudents?: number;
  passThreshold?: number;
}): Promise<{ stdout: string; stderr: string; summary: TypedAssessmentEvalSummary }> {
  const { queryId, taskId } = params;
  const repoRoot = resolveRepoRoot();
  const taskDir = path.join(repoRoot, "outputs", queryId, taskId);
  const itemPath = await findParsonsJson(taskDir, taskId);

  if (!itemPath) {
    throw new Error(`No Parsons item found for ${queryId}/${taskId}.`);
  }

  const pythonBin = existsSync(path.join(repoRoot, "pytask", "bin", "python"))
    ? path.join(repoRoot, "pytask", "bin", "python")
    : "python3";

  const args = [
    "-m",
    "code.main_typed_assessment_eval",
    "--item-path",
    itemPath,
    "--num-students",
    String(params.numStudents ?? 20),
    "--model",
    params.model ?? "gpt-4o-mini-2024-07-18",
    "--temperature",
    String(params.temperature ?? 1.0),
    "--pass-threshold",
    String(params.passThreshold ?? 50)
  ];

  const env = {
    ...process.env,
    PYTHONPATH: repoRoot,
    PATH: `/opt/homebrew/bin:${process.env.PATH ?? ""}`
  };

  const { stdout, stderr } = await execFileAsync(pythonBin, args, {
    cwd: repoRoot,
    env,
    maxBuffer: 10 * 1024 * 1024
  });

  const summary = await loadParsonsEval(taskDir, taskId);
  if (!summary) {
    throw new Error("Evaluation finished but no summary.json was produced.");
  }

  return { stdout, stderr, summary };
}
