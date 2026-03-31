import { existsSync } from "node:fs";
import { appendFile, mkdir } from "node:fs/promises";
import path from "node:path";
import type { StudentAttemptRecord, StudentTelemetryEvent } from "@/src/types";

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

async function ensureAnalyticsDir(): Promise<string> {
  const repoRoot = resolveRepoRoot();
  const analyticsDir = path.join(repoRoot, "outputs", "learning_analytics");
  await mkdir(analyticsDir, { recursive: true });
  return analyticsDir;
}

export async function recordTelemetryEvents(events: StudentTelemetryEvent[]): Promise<void> {
  if (events.length === 0) {
    return;
  }

  const analyticsDir = await ensureAnalyticsDir();
  const filePath = path.join(analyticsDir, "events.jsonl");
  const lines = events.map((event) => JSON.stringify(event)).join("\n") + "\n";
  await appendFile(filePath, lines, "utf8");
}

export async function recordAttemptRecord(record: StudentAttemptRecord): Promise<void> {
  const analyticsDir = await ensureAnalyticsDir();
  const filePath = path.join(analyticsDir, "attempts.jsonl");
  await appendFile(filePath, `${JSON.stringify(record)}\n`, "utf8");
}
