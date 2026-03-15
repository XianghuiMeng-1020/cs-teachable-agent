// API Base URL: 使用 Railway 后端（支持本地开发和生产环境）
const API_BASE = "https://cs-teachable-agent-production.up.railway.app/api";

const DEFAULT_TIMEOUT_MS = 30_000;
const MAX_RETRIES = 3;
const RETRY_DELAY_MS = 1_500;

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

/** Network status callbacks */
let onNetworkStatusChange: ((isOnline: boolean) => void) | null = null;
export function setOnNetworkStatusChange(fn: ((isOnline: boolean) => void) | null) {
  onNetworkStatusChange = fn;
}

/** Retry callback for UI feedback */
let onRetry: ((attempt: number, maxRetries: number) => void) | null = null;
export function setOnRetry(fn: ((attempt: number, maxRetries: number) => void) | null) {
  onRetry = fn;
}

function headers(): HeadersInit {
  const h: HeadersInit = { "Content-Type": "application/json" };
  if (token) h["Authorization"] = `Bearer ${token}`;
  return h;
}

function isNetworkError(err: unknown): boolean {
  if (err instanceof TypeError) {
    const msg = err.message.toLowerCase();
    return msg.includes("failed to fetch") || 
           msg.includes("load failed") ||
           msg.includes("network") ||
           msg.includes("internet");
  }
  return false;
}

function isRetryable(method: string, status: number, err?: unknown): boolean {
  if (isNetworkError(err)) return true;
  if (method !== "GET" && method !== "POST") return false;
  if (status >= 500 && status < 600) return true;
  if (status === 429) return true; // Rate limited
  if (status === 0) return true; // Network error
  return false;
}

function getErrorMessage(err: unknown, status?: number): string {
  if (isNetworkError(err)) {
    return "Network connection failed. Please check your internet connection and try again.";
  }
  if (err instanceof Error) {
    if (err.name === "AbortError") {
      return "Request timed out. The server may be busy. Please try again.";
    }
    return err.message;
  }
  if (status === 429) return "Too many requests. Please wait a moment and try again.";
  if (status === 500) return "Server error. Our team has been notified.";
  if (status === 503) return "Service temporarily unavailable. Please try again later.";
  return "An unexpected error occurred. Please try again.";
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
      // Notify retry attempt
      if (attempt > 0) {
        onRetry?.(attempt, MAX_RETRIES);
      }
      
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
        throw new Error(text || getErrorMessage(null, lastRes.status));
      }
      
      if (lastRes.ok) return lastRes;
      lastErr = new Error(await lastRes.text());
    } catch (err) {
      lastErr = err;
      
      // Handle abort error
      if (err instanceof Error && err.name === "AbortError") {
        throw new Error("Request timed out. Please try again.");
      }
      
      // Check if we should retry
      const shouldRetry = attempt < MAX_RETRIES && isRetryable(method, lastRes?.status ?? 0, err);
      
      if (shouldRetry) {
        // Exponential backoff with jitter
        const delay = RETRY_DELAY_MS * Math.pow(2, attempt) + Math.random() * 1000;
        await new Promise((r) => setTimeout(r, delay));
        continue;
      }
      
      // Final error - provide helpful message
      throw new Error(getErrorMessage(err, lastRes?.status));
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

export async function analyzeTeaching(taId: number, student_input: string): Promise<{ pattern: string; feedback: string; suggestions: string[] }> {
  const r = await apiFetch(`/ta/${taId}/analyze-teaching`, {
    method: "POST",
    headers: headers(),
    body: JSON.stringify({ student_input }),
  });
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

export interface TeachStreamCallbacks {
  onChunk?: (text: string) => void;
}

/** Stream TA response via SSE. Calls onChunk for each chunk; resolves with final { ta_response, interpreted_units, topic_taught }. */
export async function teachStream(
  taId: number,
  student_input: string,
  callbacks: TeachStreamCallbacks = {}
): Promise<{ ta_response: string; interpreted_units: string[]; topic_taught: string }> {
  const { onChunk } = callbacks;
  const url = `${API_BASE}/ta/${taId}/teach/stream`;
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...(getToken() ? { Authorization: `Bearer ${getToken()}` } : {}) },
    body: JSON.stringify({ student_input }),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `HTTP ${res.status}`);
  }
  const reader = res.body?.getReader();
  if (!reader) throw new Error("No response body");
  const dec = new TextDecoder();
  let buffer = "";
  let donePayload: { ta_response?: string; interpreted_units?: string[]; topic_taught?: string } = {};
  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += dec.decode(value, { stream: true });
    const lines = buffer.split("\n\n");
    buffer = lines.pop() ?? "";
    for (const line of lines) {
      if (line.startsWith("data: ")) {
        try {
          const data = JSON.parse(line.slice(6)) as { type: string; text?: string; ta_response?: string; interpreted_units?: string[]; topic_taught?: string };
          if (data.type === "chunk" && data.text != null && onChunk) onChunk(data.text);
          if (data.type === "done") donePayload = { ta_response: data.ta_response, interpreted_units: data.interpreted_units, topic_taught: data.topic_taught };
        } catch {
          // skip malformed
        }
      }
    }
  }
  if (buffer.startsWith("data: ")) {
    try {
      const data = JSON.parse(buffer.slice(6)) as { type: string; ta_response?: string; interpreted_units?: string[]; topic_taught?: string };
      if (data.type === "done") donePayload = { ta_response: data.ta_response, interpreted_units: data.interpreted_units, topic_taught: data.topic_taught };
    } catch {
      // skip
    }
  }
  return {
    ta_response: donePayload.ta_response ?? "",
    interpreted_units: donePayload.interpreted_units ?? [],
    topic_taught: donePayload.topic_taught ?? "",
  };
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
  topic_group: string;
  prerequisites: string[];
  difficulty: number;
  estimated_minutes: number;
}

export interface PathSummary {
  total_estimated_minutes: number;
  average_difficulty: number;
  confidence: number;
  rationale: string;
  path_length: number;
}

export interface LearningPathResponse {
  recommended: LearningPathItem[];
  path_summary?: PathSummary;
  learned_count: number;
  total_count: number;
  estimated_minutes_remaining: number;
}

export async function getLearningPath(taId: number): Promise<LearningPathResponse> {
  const r = await apiFetch(`/ta/${taId}/learning-path`, { headers: headers() });
  return r.json();
}
