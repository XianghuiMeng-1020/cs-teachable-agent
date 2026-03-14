// API Base URL: 开发环境用相对路径（Vite 代理），生产环境用环境变量或绝对路径
const API_BASE = import.meta.env.VITE_API_URL || "/api";

let token: string | null = null;

export function setToken(t: string | null) {
  token = t;
}

export function getToken(): string | null {
  return token;
}

function headers(): HeadersInit {
  const h: HeadersInit = { "Content-Type": "application/json" };
  if (token) h["Authorization"] = `Bearer ${token}`;
  return h;
}

export async function register(username: string, password: string, role = "student") {
  const r = await fetch(`${API_BASE}/auth/register`, {
    method: "POST",
    headers: headers(),
    body: JSON.stringify({ username, password, role }),
  });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function login(username: string, password: string) {
  const r = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: headers(),
    body: JSON.stringify({ username, password }),
  });
  if (!r.ok) throw new Error(await r.text());
  const data = await r.json();
  if (data.access_token) setToken(data.access_token);
  return data;
}

export async function me() {
  const r = await fetch(`${API_BASE}/auth/me`, { headers: headers() });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function listTA() {
  const r = await fetch(`${API_BASE}/ta`, { headers: headers() });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function createTA(domain_id = "python", name?: string) {
  const r = await fetch(`${API_BASE}/ta`, {
    method: "POST",
    headers: headers(),
    body: JSON.stringify({ domain_id, name }),
  });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function getTA(taId: number) {
  const r = await fetch(`${API_BASE}/ta/${taId}`, { headers: headers() });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function teach(taId: number, student_input: string) {
  const r = await fetch(`${API_BASE}/ta/${taId}/teach`, {
    method: "POST",
    headers: headers(),
    body: JSON.stringify({ student_input }),
  });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function runTest(taId: number, problem_id?: string) {
  const r = await fetch(`${API_BASE}/ta/${taId}/test`, {
    method: "POST",
    headers: headers(),
    body: JSON.stringify(problem_id ? { problem_id } : {}),
  });
  if (!r.ok) throw new Error(await r.text());
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
  const r = await fetch(`${API_BASE}/ta/${taId}/test/comprehensive`, {
    method: "POST",
    headers: headers(),
    body: JSON.stringify({}),
  });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function getState(taId: number) {
  const r = await fetch(`${API_BASE}/ta/${taId}/state`, { headers: headers() });
  if (!r.ok) throw new Error(await r.text());
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
  const r = await fetch(`${API_BASE}/ta/${taId}/mastery`, { headers: headers() });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function getProblems(taId: number) {
  const r = await fetch(`${API_BASE}/ta/${taId}/problems`, { headers: headers() });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function getTrace(taId: number) {
  const r = await fetch(`${API_BASE}/ta/${taId}/trace`, { headers: headers() });
  if (!r.ok) throw new Error(await r.text());
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
  const r = await fetch(`${API_BASE}/ta/${taId}/misconceptions`, { headers: headers() });
  if (!r.ok) throw new Error(await r.text());
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
  const r = await fetch(`${API_BASE}/ta/${taId}/history${q ? `?${q}` : ""}`, { headers: headers() });
  if (!r.ok) throw new Error(await r.text());
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
  const r = await fetch(`${API_BASE}/ta/${taId}/messages`, { headers: headers() });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function teacherStudents() {
  const r = await fetch(`${API_BASE}/teacher/students`, { headers: headers() });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function teacherAnalytics() {
  const r = await fetch(`${API_BASE}/teacher/analytics`, { headers: headers() });
  if (!r.ok) throw new Error(await r.text());
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
  const r = await fetch(`${API_BASE}/teacher/transcripts${q ? `?${q}` : ""}`, { headers: headers() });
  if (!r.ok) throw new Error(await r.text());
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
  const r = await fetch(`${API_BASE}/teacher/transcripts/${sessionId}`, { headers: headers() });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function teacherTranscriptsExport(sessionId?: number): Promise<Blob> {
  const q = sessionId != null ? `?session_id=${sessionId}` : "";
  const r = await fetch(`${API_BASE}/teacher/transcripts/export${q}`, { headers: headers() });
  if (!r.ok) throw new Error(await r.text());
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
  const r = await fetch(`${API_BASE}/teacher/student/${userId}/detail`, { headers: headers() });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}
