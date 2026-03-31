import { existsSync } from "node:fs";
import { readdir, readFile } from "node:fs/promises";
import path from "node:path";

type ItemType = "parsons" | "dropdown" | "execution-trace";

type SourceTaskRow = {
  taskId: string;
  genConsistency: number | null;
  qTestsuite: number | null;
  qContext: number | null;
  totalNumStu: number | null;
  numPassedStu: number | null;
  studentPassRate: number | null;
  pyTaskSyn50Passed: boolean;
};

type ItemRecord = {
  queryId: string;
  taskId: string;
  itemId: string;
  itemType: ItemType;
  title: string;
  theme: string | null;
  concepts: string[];
  validationPassed: boolean | null;
  aiPassRate: number | null;
  aiPopulationPassed: boolean | null;
  sourceStudentPassRate: number | null;
  genConsistency: number | null;
  qTestsuite: number | null;
  qContext: number | null;
  pyTaskSyn50Passed: boolean;
};

type QueryMetrics = {
  queryId: string;
  sourceTaskCount: number;
  typedItemCount: number;
  evaluatedItemCount: number;
  lowAiItemCount: number;
  avgAiPassRate: number | null;
  avgStudentPassRate: number | null;
  genConsistencyRate: number | null;
  qTestsuiteRate: number | null;
  qContextRate: number | null;
  pyTaskSyn50Count: number;
};

type TypeOverview = {
  itemType: ItemType;
  totalItems: number;
  evaluatedItems: number;
  lowAiItems: number;
  avgAiPassRate: number | null;
  avgStudentPassRate: number | null;
};

type ThemeOverview = {
  theme: string;
  totalItems: number;
  evaluatedItems: number;
  lowAiItems: number;
  avgAiPassRate: number | null;
};

type TelemetryAttempt = {
  attemptId: string;
  sessionId: string;
  attemptNumber: number;
  queryId: string;
  taskId: string;
  itemId: string;
  itemType: ItemType;
  startedAt: string;
  submittedAt: string;
  durationMs: number;
  focusLossCount: number;
  isCorrect: boolean;
  score: number;
};

type TelemetryEvent = {
  eventType: string;
  eventTime: string;
  sessionId: string;
  attemptId?: string | null;
  queryId?: string | null;
  taskId?: string | null;
  itemType?: string | null;
  payload?: Record<string, unknown>;
};

export type MetricsDashboardData = {
  generatedAt: string;
  totals: {
    queries: number;
    sourceTasks: number;
    typedItems: number;
    evaluatedItems: number;
    lowAiItems: number;
    avgAiPassRate: number | null;
    avgStudentPassRate: number | null;
    telemetryEvents: number;
    telemetryAttempts: number;
  };
  typeOverview: TypeOverview[];
  queryOverview: QueryMetrics[];
  themeOverview: ThemeOverview[];
  hardestItems: ItemRecord[];
  easiestItems: ItemRecord[];
  aiPassDistribution: Array<{ bucket: string; parsons: number; dropdown: number; executionTrace: number }>;
  pipeline: {
    avgGenConsistencyRate: number | null;
    avgQTestsuiteRate: number | null;
    avgQContextRate: number | null;
    pyTaskSyn50Coverage: number | null;
  };
  telemetry: {
    available: boolean;
    totalEvents: number;
    totalAttempts: number;
    focusLossCount: number;
    resumeCount: number;
    avgAttemptDurationMs: number | null;
    avgAttemptScore: number | null;
    eventBreakdown: Array<{ eventType: string; count: number }>;
    recentAttempts: TelemetryAttempt[];
    recentFocusEvents: TelemetryEvent[];
  };
};

function isNoise(name: string): boolean {
  return name.startsWith("._") || name === "__pycache__";
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

function average(values: number[]): number | null {
  if (values.length === 0) {
    return null;
  }
  return Number((values.reduce((sum, value) => sum + value, 0) / values.length).toFixed(1));
}

function percentage(numerator: number, denominator: number): number | null {
  if (denominator <= 0) {
    return null;
  }
  return Number(((numerator / denominator) * 100).toFixed(1));
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

async function parseJsonLinesIfExists<T>(filePath: string): Promise<T[]> {
  const text = await readFileIfExists(filePath);
  if (!text) {
    return [];
  }

  return text
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line.length > 0)
    .map((line) => JSON.parse(line) as T);
}

function sortByNumericSuffix<T extends string>(values: T[]): T[] {
  return [...values].sort((left, right) => {
    const leftIndex = Number.parseInt(left.split("_").at(-1) ?? "0", 10);
    const rightIndex = Number.parseInt(right.split("_").at(-1) ?? "0", 10);
    return leftIndex - rightIndex;
  });
}

function itemTypeFromFileName(fileName: string): ItemType | null {
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

async function loadSourceRows(queryDir: string): Promise<Map<string, SourceTaskRow>> {
  const rows = new Map<string, SourceTaskRow>();
  const resultsText = await readFileIfExists(path.join(queryDir, "results.csv"));
  if (!resultsText) {
    return rows;
  }

  for (const row of parseCsv(resultsText)) {
    const taskId = row.task;
    if (!taskId) {
      continue;
    }
    const totalNumStu = toNumber(row.total_num_stu);
    const numPassedStu = toNumber(row.num_passed_stu);
    const studentPassRate =
      totalNumStu !== null && totalNumStu > 0 && numPassedStu !== null ? (numPassedStu / totalNumStu) * 100 : null;
    const genConsistency = toNumber(row.gen_consistency);
    const qTestsuite = toNumber(row["Q-Testsuite"]);
    const qContext = toNumber(row["Q-Context"]);

    rows.set(taskId, {
      taskId,
      genConsistency,
      qTestsuite,
      qContext,
      totalNumStu,
      numPassedStu,
      studentPassRate,
      pyTaskSyn50Passed: genConsistency === 1 && qTestsuite === 1 && qContext === 1 && (studentPassRate ?? 0) >= 50
    });
  }

  return rows;
}

async function listTaskDirs(queryDir: string): Promise<string[]> {
  const entries = await readdir(queryDir, { withFileTypes: true });
  return sortByNumericSuffix(
    entries.filter((entry) => entry.isDirectory() && /^task_\d+$/.test(entry.name) && !isNoise(entry.name)).map((entry) => entry.name)
  );
}

async function loadItemRecord(taskDir: string, queryId: string, taskId: string, sourceRow: SourceTaskRow | undefined): Promise<ItemRecord[]> {
  const entries = await readdir(taskDir, { withFileTypes: true });
  const jsonFiles = entries.filter((entry) => entry.isFile() && !isNoise(entry.name) && itemTypeFromFileName(entry.name));
  const records: ItemRecord[] = [];

  for (const entry of jsonFiles) {
    const itemType = itemTypeFromFileName(entry.name);
    if (!itemType) {
      continue;
    }

    const itemPath = path.join(taskDir, entry.name);
    const raw = await readJsonIfExists<Record<string, unknown>>(itemPath);
    if (!raw) {
      continue;
    }

    const metadata = (raw.metadata ?? {}) as Record<string, unknown>;
    const validation = (raw.validation ?? {}) as Record<string, unknown>;
    const evalSummary = await readJsonIfExists<Record<string, unknown>>(
      path.join(taskDir, `${path.basename(entry.name, ".json")}-eval`, "summary.json")
    );

    records.push({
      queryId,
      taskId,
      itemId: String(raw.item_id ?? `${taskId}-${itemType}`),
      itemType,
      title: String(raw.title ?? `${taskId}-${itemType}`),
      theme: typeof metadata.theme === "string" ? metadata.theme : null,
      concepts: Array.isArray(metadata.concepts) ? metadata.concepts.map((value) => String(value)) : [],
      validationPassed: typeof validation.passed === "boolean" ? validation.passed : null,
      aiPassRate: typeof evalSummary?.pass_rate === "number" ? evalSummary.pass_rate : null,
      aiPopulationPassed: typeof evalSummary?.population_passed === "boolean" ? evalSummary.population_passed : null,
      sourceStudentPassRate: sourceRow?.studentPassRate ?? null,
      genConsistency: sourceRow?.genConsistency ?? null,
      qTestsuite: sourceRow?.qTestsuite ?? null,
      qContext: sourceRow?.qContext ?? null,
      pyTaskSyn50Passed: sourceRow?.pyTaskSyn50Passed ?? false
    });
  }

  return records;
}

function bucketLabel(passRate: number): string {
  if (passRate < 25) {
    return "0-25";
  }
  if (passRate < 50) {
    return "25-50";
  }
  if (passRate < 75) {
    return "50-75";
  }
  return "75-100";
}

export async function getMetricsDashboardData(): Promise<MetricsDashboardData> {
  const repoRoot = resolveRepoRoot();
  const outputsDir = path.join(repoRoot, "outputs");
  const queryEntries = await readdir(outputsDir, { withFileTypes: true });
  const queryIds = sortByNumericSuffix(
    queryEntries.filter((entry) => entry.isDirectory() && /^query_\d+$/.test(entry.name) && !isNoise(entry.name)).map((entry) => entry.name)
  );

  const items: ItemRecord[] = [];
  const queryOverview: QueryMetrics[] = [];

  for (const queryId of queryIds) {
    const queryDir = path.join(outputsDir, queryId);
    const taskDirs = await listTaskDirs(queryDir);
    const sourceRows = await loadSourceRows(queryDir);

    const queryItems: ItemRecord[] = [];
    for (const taskId of taskDirs) {
      const taskDir = path.join(queryDir, taskId);
      const sourceRow = sourceRows.get(taskId);
      const taskItems = await loadItemRecord(taskDir, queryId, taskId, sourceRow);
      queryItems.push(...taskItems);
    }

    items.push(...queryItems);

    const sourceTaskRows = [...sourceRows.values()];
    queryOverview.push({
      queryId,
      sourceTaskCount: taskDirs.length,
      typedItemCount: queryItems.length,
      evaluatedItemCount: queryItems.filter((item) => item.aiPassRate !== null).length,
      lowAiItemCount: queryItems.filter((item) => item.aiPassRate !== null && item.aiPassRate <= 75).length,
      avgAiPassRate: average(queryItems.map((item) => item.aiPassRate).filter((value): value is number => value !== null)),
      avgStudentPassRate: average(
        sourceTaskRows.map((row) => row.studentPassRate).filter((value): value is number => value !== null)
      ),
      genConsistencyRate: percentage(
        sourceTaskRows.filter((row) => row.genConsistency === 1).length,
        sourceTaskRows.length
      ),
      qTestsuiteRate: percentage(
        sourceTaskRows.filter((row) => row.qTestsuite === 1).length,
        sourceTaskRows.length
      ),
      qContextRate: percentage(
        sourceTaskRows.filter((row) => row.qContext === 1).length,
        sourceTaskRows.length
      ),
      pyTaskSyn50Count: sourceTaskRows.filter((row) => row.pyTaskSyn50Passed).length
    });
  }

  const typeOverview: TypeOverview[] = (["parsons", "dropdown", "execution-trace"] as ItemType[]).map((itemType) => {
    const subset = items.filter((item) => item.itemType === itemType);
    return {
      itemType,
      totalItems: subset.length,
      evaluatedItems: subset.filter((item) => item.aiPassRate !== null).length,
      lowAiItems: subset.filter((item) => item.aiPassRate !== null && item.aiPassRate <= 75).length,
      avgAiPassRate: average(subset.map((item) => item.aiPassRate).filter((value): value is number => value !== null)),
      avgStudentPassRate: average(
        subset.map((item) => item.sourceStudentPassRate).filter((value): value is number => value !== null)
      )
    };
  });

  const themeMap = new Map<string, ItemRecord[]>();
  for (const item of items) {
    const theme = item.theme ?? "Unknown";
    const current = themeMap.get(theme) ?? [];
    current.push(item);
    themeMap.set(theme, current);
  }
  const themeOverview: ThemeOverview[] = [...themeMap.entries()]
    .map(([theme, themeItems]) => ({
      theme,
      totalItems: themeItems.length,
      evaluatedItems: themeItems.filter((item) => item.aiPassRate !== null).length,
      lowAiItems: themeItems.filter((item) => item.aiPassRate !== null && item.aiPassRate <= 75).length,
      avgAiPassRate: average(themeItems.map((item) => item.aiPassRate).filter((value): value is number => value !== null))
    }))
    .sort((left, right) => right.totalItems - left.totalItems);

  const evaluatedItems = items.filter((item) => item.aiPassRate !== null);
  const hardestItems = [...evaluatedItems]
    .sort((left, right) => (left.aiPassRate ?? 101) - (right.aiPassRate ?? 101))
    .slice(0, 8);
  const easiestItems = [...evaluatedItems]
    .sort((left, right) => (right.aiPassRate ?? -1) - (left.aiPassRate ?? -1))
    .slice(0, 8);

  const distributionBuckets = ["0-25", "25-50", "50-75", "75-100"] as const;
  const distributionMap = new Map<string, { bucket: string; parsons: number; dropdown: number; executionTrace: number }>();
  for (const bucket of distributionBuckets) {
    distributionMap.set(bucket, { bucket, parsons: 0, dropdown: 0, executionTrace: 0 });
  }
  for (const item of evaluatedItems) {
    const bucket = bucketLabel(item.aiPassRate ?? 0);
    const record = distributionMap.get(bucket);
    if (!record) {
      continue;
    }
    if (item.itemType === "parsons") {
      record.parsons += 1;
    } else if (item.itemType === "dropdown") {
      record.dropdown += 1;
    } else {
      record.executionTrace += 1;
    }
  }

  const eventsPath = path.join(outputsDir, "learning_analytics", "events.jsonl");
  const attemptsPath = path.join(outputsDir, "learning_analytics", "attempts.jsonl");
  const telemetryEvents = await parseJsonLinesIfExists<TelemetryEvent>(eventsPath);
  const telemetryAttempts = await parseJsonLinesIfExists<TelemetryAttempt>(attemptsPath);

  const eventBreakdownMap = new Map<string, number>();
  for (const event of telemetryEvents) {
    eventBreakdownMap.set(event.eventType, (eventBreakdownMap.get(event.eventType) ?? 0) + 1);
  }

  const sourceRowsAll = queryOverview;
  return {
    generatedAt: new Date().toISOString(),
    totals: {
      queries: queryIds.length,
      sourceTasks: queryOverview.reduce((sum, query) => sum + query.sourceTaskCount, 0),
      typedItems: items.length,
      evaluatedItems: evaluatedItems.length,
      lowAiItems: evaluatedItems.filter((item) => (item.aiPassRate ?? 101) <= 75).length,
      avgAiPassRate: average(evaluatedItems.map((item) => item.aiPassRate ?? 0)),
      avgStudentPassRate: average(
        items.map((item) => item.sourceStudentPassRate).filter((value): value is number => value !== null)
      ),
      telemetryEvents: telemetryEvents.length,
      telemetryAttempts: telemetryAttempts.length
    },
    typeOverview,
    queryOverview,
    themeOverview,
    hardestItems,
    easiestItems,
    aiPassDistribution: distributionBuckets.map((bucket) => distributionMap.get(bucket)!),
    pipeline: {
      avgGenConsistencyRate: average(
        sourceRowsAll.map((query) => query.genConsistencyRate).filter((value): value is number => value !== null)
      ),
      avgQTestsuiteRate: average(
        sourceRowsAll.map((query) => query.qTestsuiteRate).filter((value): value is number => value !== null)
      ),
      avgQContextRate: average(
        sourceRowsAll.map((query) => query.qContextRate).filter((value): value is number => value !== null)
      ),
      pyTaskSyn50Coverage: percentage(
        sourceRowsAll.filter((query) => query.pyTaskSyn50Count > 0).length,
        sourceRowsAll.length
      )
    },
    telemetry: {
      available: telemetryEvents.length > 0 || telemetryAttempts.length > 0,
      totalEvents: telemetryEvents.length,
      totalAttempts: telemetryAttempts.length,
      focusLossCount: telemetryEvents.filter((event) => event.eventType === "focus_lost").length,
      resumeCount: telemetryEvents.filter((event) => event.eventType === "resume_clicked").length,
      avgAttemptDurationMs: average(
        telemetryAttempts.map((attempt) => attempt.durationMs).filter((value) => Number.isFinite(value))
      ),
      avgAttemptScore: average(
        telemetryAttempts.map((attempt) => attempt.score * 100).filter((value) => Number.isFinite(value))
      ),
      eventBreakdown: [...eventBreakdownMap.entries()]
        .map(([eventType, count]) => ({ eventType, count }))
        .sort((left, right) => right.count - left.count),
      recentAttempts: [...telemetryAttempts]
        .sort((left, right) => right.submittedAt.localeCompare(left.submittedAt))
        .slice(0, 8),
      recentFocusEvents: telemetryEvents
        .filter((event) => event.eventType === "focus_lost")
        .sort((left, right) => right.eventTime.localeCompare(left.eventTime))
        .slice(0, 8)
    }
  };
}
