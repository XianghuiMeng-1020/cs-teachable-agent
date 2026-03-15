// API Base URL: 使用 Railway 后端（支持本地开发和生产环境）
const API_BASE = "https://cs-teachable-agent-production.up.railway.app/api";

const DEFAULT_TIMEOUT_MS = 30_000;
const MAX_RETRIES = 2;
const RETRY_DELAY_MS = 1_000;

let token: string | null = null;

export function setToken(t: string | null) {
  token = t;
}

export function getToken(): string | null {
  return token;
}

/** Called on 401 so app can clear auth state and redirect */
let onUnauthorized: (() => void) | null = null;
export function setOnUnauthorized(fn: (() => void) | null) {
  onUnauthorized = fn;
}

function headers(): HeadersInit {
  const h: HeadersInit = { "Content-Type": "application/json" };
  if (token) h["Authorization"] = `Bearer ${token}`;
  return h;
}

function isRetryable(method: string, status: number, err?: unknown): boolean {
  if (method !== "GET") return false;
  if (status >= 500 && status < 600) return true;
  if (err instanceof TypeError && (err.message === "Failed to fetch" || err.message === "Load failed")) return true;
  return false;
}

async function fetchWithTimeout(
  url: string,
  init: RequestInit,
  timeoutMs: number = DEFAULT_TIMEOUT_MS
): Promise<Response> {
  const ac = new AbortController();
  const id = setTimeout(() => ac.abort(), timeoutMs);
  try {
    const r = await fetch(url, { ...init, signal: ac.signal });
    return r;
  } finally {
    clearTimeout(id);
  }
}

async function apiFetch(
  url: string,
  init: RequestInit & { timeout?: number; skipRetry?: boolean } = {}
): Promise<Response> {
  const { timeout = DEFAULT_TIMEOUT_MS, skipRetry = false, ...fetchInit } = init;
  const method = (fetchInit.method || "GET").toUpperCase();
  let lastErr: unknown;
  let lastRes: Response | null = null;
  for (let attempt = 0; attempt <= (skipRetry ? 0 : MAX_RETRIES); attempt++) {
    try {
      lastRes = await fetchWithTimeout(`${API_BASE}${url}`, fetchInit, timeout);
      if (lastRes.status === 401) {
        setToken(null);
        onUnauthorized?.();
        const text = await lastRes.text();
        let msg = text;
        try {
          const o = JSON.parse(text) as { detail?: string };
          if (typeof o.detail === "string") msg = o.detail;
        } catch {
          // use text
        }
        throw new Error(msg);
      }
      if (!lastRes.ok && !isRetryable(method, lastRes.status)) {
        const text = await lastRes.text();
        throw new Error(text);
      }
      if (lastRes.ok) return lastRes;
      lastErr = new Error(await lastRes.text());
    } catch (err) {
      lastErr = err;
      if (err instanceof Error && err.name === "AbortError") throw new Error("Request timed out. Please try again.");
      if (attempt < MAX_RETRIES && isRetryable(method, 0, err)) {
        await new Promise((r) => setTimeout(r, RETRY_DELAY_MS));
        continue;
      }
      throw err;
    }
  }
  if (lastRes) return lastRes;
  throw lastErr;
}

export async function register(username: string, password: string, role = "student") {
  const r = await apiFetch("/auth/register", {
    method: "POST",
    headers: headers(),
    body: JSON.stringify({ username, password, role }),
    skipRetry: true,
  });
  const data = await r.json();
  return data;
}

export async function login(username: string, password: string) {
  const r = await apiFetch("/auth/login", {
    method: "POST",
    headers: headers(),
    body: JSON.stringify({ username, password }),
    skipRetry: true,
  });
  const data = await r.json();
  if (data.access_token) setToken(data.access_token);
  return data;
}

export async function me() {
  const r = await apiFetch("/auth/me", { headers: headers() });
  return r.json();
}

export async function listTA() {
  const r = await apiFetch("/ta", { headers: headers() });
  return r.json();
}

export async function createTA(domain_id = "python", name?: string) {
  const r = await apiFetch("/ta", {
    method: "POST",
    headers: headers(),
    body: JSON.stringify({ domain_id, name }),
  });
  return r.json();
}

export async function getTA(taId: number) {
  const r = await apiFetch(`/ta/${taId}`, { headers: headers() });
  return r.json();
}

export async function teach(taId: number, student_input: string) {
  const r = await apiFetch(`/ta/${taId}/teach`, {
    method: "POST",
    headers: headers(),
    body: JSON.stringify({ student_input }),
  });
  return r.json();
}

export async function runTest(taId: number, problem_id?: string) {
  const r = await apiFetch(`/ta/${taId}/test`, {
    method: "POST",
    headers: headers(),
    body: JSON.stringify(problem_id ? { problem_id } : {}),
  });
  return r.json();
}

export interface ComprehensiveTestResultItem {
  problem_id: string;
  passed: boolean;
  problem_statement: string;
}

export interface ComprehensiveTestResponse {
  total_run: number;
  total_passed: number;
  results: ComprehensiveTestResultItem[];
  overall_summary: string;
}

export async function runTestComprehensive(taId: number): Promise<ComprehensiveTestResponse> {
  const r = await apiFetch(`/ta/${taId}/test/comprehensive`, {
    method: "POST",
    headers: headers(),
    body: JSON.stringify({}),
  });
  return r.json();
}

export async function getState(taId: number) {
  const r = await apiFetch(`/ta/${taId}/state`, { headers: headers() });
  return r.json();
}

export interface MasteryResponse {
  selected_problem_id: string | null;
  required_kus: string[];
  learned_kus_at_attempt: string[];
  pass_fail: string | null;
  overall_summary: string;
  per_problem_interpretation?: string | null;
  ta_code_preview?: string | null;
  mastery_percent?: number | null;
  pass_rate?: number | null;
  test_count?: number | null;
}

export async function getMastery(taId: number): Promise<MasteryResponse> {
  const r = await apiFetch(`/ta/${taId}/mastery`, { headers: headers() });
  return r.json();
}

export interface ProblemsResponse {
  problems: Array<{
    problem_id: string;
    problem_statement: string;
    difficulty?: string;
    knowledge_units_required?: string[];
  }>;
  eligible_ids: string[];
  learned_unit_ids: string[];
  required_kus: string[];
}

export async function getProblems(taId: number): Promise<ProblemsResponse> {
  const r = await apiFetch(`/ta/${taId}/problems`, { headers: headers() });
  return r.json();
}

export async function getTrace(taId: number) {
  const r = await apiFetch(`/ta/${taId}/trace`, { headers: headers() });
  return r.json();
}

export interface MisconceptionDetailDto {
  id: string;
  description: string;
  affected_units: string[];
  remediation_hint: string;
  status: string;
  activated_at?: string | null;
}

export interface MisconceptionsResponse {
  active_misconception_ids: string[];
  misconceptions: MisconceptionDetailDto[];
}

export async function getMisconceptions(taId: number): Promise<MisconceptionsResponse> {
  const r = await apiFetch(`/ta/${taId}/misconceptions`, { headers: headers() });
  return r.json();
}

export interface HistoryItem {
  id: string;
  type: string;
  title: string;
  description: string;
  timestamp: string;
  metadata?: Record<string, unknown>;
}

export interface HistoryResponse {
  items: HistoryItem[];
  total: number;
  page: number;
  per_page: number;
}

export async function getHistory(
  taId: number,
  params?: { page?: number; per_page?: number; type?: string }
): Promise<HistoryResponse> {
  const sp = new URLSearchParams();
  if (params?.page != null) sp.set("page", String(params.page));
  if (params?.per_page != null) sp.set("per_page", String(params.per_page));
  if (params?.type != null) sp.set("type", params.type);
  const q = sp.toString();
  const r = await apiFetch(`/ta/${taId}/history${q ? `?${q}` : ""}`, { headers: headers() });
  return r.json();
}

export interface ChatMessageDto {
  role: "student" | "ta";
  content: string;
  timestamp?: string;
}

export interface GetMessagesResponse {
  messages: ChatMessageDto[];
}

export async function getMessages(taId: number): Promise<GetMessagesResponse> {
  const r = await apiFetch(`/ta/${taId}/messages`, { headers: headers() });
  return r.json();
}

export async function teacherStudents() {
  const r = await apiFetch("/teacher/students", { headers: headers() });
  return r.json();
}

export async function teacherAnalytics() {
  const r = await apiFetch("/teacher/analytics", { headers: headers() });
  return r.json();
}

export interface TranscriptSessionSummary {
  session_id: number;
  student: { id: number; username: string };
  ta_id: number;
  domain_id: string;
  message_count: number;
  kus_covered: string[];
  started_at: string;
  ended_at?: string | null;
}

export interface TranscriptListResponse {
  items: TranscriptSessionSummary[];
  total: number;
  page: number;
  per_page: number;
}

export async function teacherTranscripts(params?: {
  page?: number;
  per_page?: number;
  student_id?: number;
  date_from?: string;
  date_to?: string;
  search?: string;
  ku?: string;
}): Promise<TranscriptListResponse> {
  const sp = new URLSearchParams();
  if (params?.page != null) sp.set("page", String(params.page));
  if (params?.per_page != null) sp.set("per_page", String(params.per_page));
  if (params?.student_id != null) sp.set("student_id", String(params.student_id));
  if (params?.date_from) sp.set("date_from", params.date_from);
  if (params?.date_to) sp.set("date_to", params.date_to);
  if (params?.search) sp.set("search", params.search);
  if (params?.ku) sp.set("ku", params.ku);
  const q = sp.toString();
  const r = await apiFetch(`/teacher/transcripts${q ? `?${q}` : ""}`, { headers: headers() });
  return r.json();
}

export interface TranscriptMessage {
  seq: number;
  type: string;
  speaker: string;
  content: string;
  interpreted_units: string[] | null;
  quality_score: number | null;
  timestamp: string;
}

export interface TranscriptDetailResponse {
  session_id: number;
  student: { id: number; username: string };
  ta: { id: number; domain_id: string };
  started_at: string;
  messages: TranscriptMessage[];
}

export async function teacherTranscriptDetail(sessionId: number): Promise<TranscriptDetailResponse> {
  const r = await apiFetch(`/teacher/transcripts/${sessionId}`, { headers: headers() });
  return r.json();
}

export async function teacherTranscriptsExport(sessionId?: number): Promise<Blob> {
  const q = sessionId != null ? `?session_id=${sessionId}` : "";
  const r = await apiFetch(`/teacher/transcripts/export${q}`, { headers: headers() });
  return r.blob();
}

export interface StudentTADetail {
  id: number;
  domain_id: string;
  learned_count: number;
  total_kus: number;
  mastery_percent: number;
  active_misconceptions: string[];
  test_count: number;
  pass_rate: number;
  last_active: string | null;
}

export interface StudentDetailResponse {
  user: { id: number; username: string; role: string; created_at?: string };
  ta_instances: StudentTADetail[];
}

export async function teacherStudentDetail(userId: number): Promise<StudentDetailResponse> {
  const r = await apiFetch(`/teacher/student/${userId}/detail`, { headers: headers() });
  return r.json();
}

export interface ConfigResponse {
  llm_configured: boolean;
  llm_provider: string | null;
  environment: string;
}

export async function getConfig(): Promise<ConfigResponse> {
  const r = await apiFetch("/config", { headers: headers() });
  return r.json();
}

export interface RunPythonResponse {
  stdout: string;
  stderr: string;
  returncode: number;
}

export async function runPythonSandbox(code: string, stdin = ""): Promise<RunPythonResponse> {
  const r = await apiFetch("/sandbox/run-python", {
    method: "POST",
    headers: headers(),
    body: JSON.stringify({ code, stdin }),
  });
  return r.json();
}

export interface GamificationAchievement {
  id: string;
  name: string;
  description: string;
  unlocked: boolean;
}

export interface GamificationResponse {
  points: number;
  level: number;
  teach_count: number;
  test_attempt_count: number;
  test_pass_count: number;
  achievements: GamificationAchievement[];
}

export async function getGamification(): Promise<GamificationResponse> {
  const r = await apiFetch("/gamification/me", { headers: headers() });
  return r.json();
}

export interface LearningPathItem {
  id: string;
  name: string;
  topic_group?: string;
  prerequisites: string[];
}

export interface LearningPathResponse {
  recommended: LearningPathItem[];
  learned_count: number;
  total_count: number;
  estimated_minutes_remaining: number;
}

export async function getLearningPath(taId: number): Promise<LearningPathResponse> {
  const r = await apiFetch(`/ta/${taId}/learning-path`, { headers: headers() });
  return r.json();
}
