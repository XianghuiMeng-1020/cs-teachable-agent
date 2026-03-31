import { getToken } from "./client";

const API_BASE = import.meta.env.VITE_API_URL
  || (import.meta.env.DEV ? "/api" : "/api");

function headers(): HeadersInit {
  const h: HeadersInit = { "Content-Type": "application/json" };
  const token = getToken();
  if (token) h["Authorization"] = `Bearer ${token}`;
  return h;
}

async function apiFetch(url: string, init: RequestInit = {}): Promise<Response> {
  const r = await fetch(`${API_BASE}${url}`, { ...init, headers: { ...headers(), ...(init.headers || {}) } });
  if (!r.ok) {
    const text = await r.text();
    throw new Error(text || `HTTP ${r.status}`);
  }
  return r;
}

// ---- Types ----

export interface AssessmentItemSummary {
  id: number;
  item_id: string;
  item_type: "parsons" | "dropdown" | "execution-trace";
  title: string;
  theme: string | null;
  concepts: string[] | null;
  ai_pass_rate: number | null;
  difficulty: number | null;
}

export interface AssessmentItemListResponse {
  items: AssessmentItemSummary[];
  total: number;
}

export interface DropdownBlank {
  blank_id: string;
  placeholder: string;
  options: string[];
}

export interface ExecutionTraceCheckpoint {
  checkpoint_id: string;
  line_number: number;
  line_excerpt: string;
  variable_name: string;
}

export interface AssessmentItemDetail {
  id: number;
  item_id: string;
  item_type: "parsons" | "dropdown" | "execution-trace";
  title: string;
  prompt: string;
  theme: string | null;
  concepts: string[];
  ai_pass_rate: number | null;
  difficulty: number | null;
  // parsons
  required_block_count?: number;
  options?: string[];
  // dropdown
  required_blank_count?: number;
  prompt_template?: string;
  blanks?: DropdownBlank[];
  // execution-trace
  required_checkpoint_count?: number;
  function_name?: string;
  function_source?: string;
  call_expression?: string;
  checkpoints?: ExecutionTraceCheckpoint[];
}

export interface GradeResponse {
  item_type: string;
  correct: boolean;
  feedback: string;
  expected_count: number;
  selected_count: number;
  correct_count: number;
  attempt_id: number | null;
}

export interface HintResponse {
  hint_id: string;
  hint_type: string;
  level: number;
  title: string;
  body: string;
  target: { kind: string; id: string; label: string } | null;
  escalation_available: boolean;
  model: string;
}

export interface AttemptHistoryItem {
  id: number;
  item_id: string;
  item_type: string;
  title: string;
  is_correct: boolean;
  score: number | null;
  correct_count: number | null;
  expected_count: number | null;
  hints_used: number;
  duration_ms: number | null;
  created_at: string | null;
}

export interface AttemptHistoryResponse {
  attempts: AttemptHistoryItem[];
  total: number;
  stats: {
    total_attempts: number;
    correct_attempts: number;
    accuracy: number;
    unique_items_solved: number;
  };
}

export interface AssessmentStats {
  total_items_available: number;
  total_attempts: number;
  correct_attempts: number;
  accuracy: number;
  unique_items_solved: number;
  progress_percent: number;
  by_type: Record<string, number>;
}

// ---- API calls ----

export async function listAssessmentItems(params?: {
  item_type?: string;
  domain_id?: string;
  max_ai_pass_rate?: number;
  concept?: string;
  limit?: number;
  offset?: number;
}): Promise<AssessmentItemListResponse> {
  const sp = new URLSearchParams();
  if (params?.item_type) sp.set("item_type", params.item_type);
  if (params?.domain_id) sp.set("domain_id", params.domain_id);
  if (params?.max_ai_pass_rate != null) sp.set("max_ai_pass_rate", String(params.max_ai_pass_rate));
  if (params?.concept) sp.set("concept", params.concept);
  if (params?.limit != null) sp.set("limit", String(params.limit));
  if (params?.offset != null) sp.set("offset", String(params.offset));
  const q = sp.toString();
  const r = await apiFetch(`/assessment/items${q ? `?${q}` : ""}`);
  return r.json();
}

export async function getAssessmentItem(itemDbId: number): Promise<AssessmentItemDetail> {
  const r = await apiFetch(`/assessment/items/${itemDbId}`);
  return r.json();
}

export async function gradeAssessmentItem(
  itemDbId: number,
  body: {
    ta_id?: number;
    selected_blocks?: string[];
    selected_answers?: Record<string, string>;
    duration_ms?: number;
    hints_used?: number;
  }
): Promise<GradeResponse> {
  const r = await apiFetch(`/assessment/items/${itemDbId}/grade`, {
    method: "POST",
    body: JSON.stringify(body),
  });
  return r.json();
}

export async function getAssessmentHint(
  itemDbId: number,
  body: {
    ta_id?: number;
    hint_type?: "understand" | "next-step" | "check-one-issue";
    level?: 1 | 2 | 3;
    selected_blocks?: string[];
    selected_answers?: Record<string, string>;
    last_feedback?: Record<string, unknown>;
    reflection?: string;
    progress_summary?: string;
    attempt_number?: number;
  }
): Promise<HintResponse> {
  const r = await apiFetch(`/assessment/items/${itemDbId}/hint`, {
    method: "POST",
    body: JSON.stringify(body),
  });
  return r.json();
}

export async function getAttemptHistory(params?: {
  ta_id?: number;
  item_type?: string;
  limit?: number;
  offset?: number;
}): Promise<AttemptHistoryResponse> {
  const sp = new URLSearchParams();
  if (params?.ta_id != null) sp.set("ta_id", String(params.ta_id));
  if (params?.item_type) sp.set("item_type", params.item_type);
  if (params?.limit != null) sp.set("limit", String(params.limit));
  if (params?.offset != null) sp.set("offset", String(params.offset));
  const q = sp.toString();
  const r = await apiFetch(`/assessment/history${q ? `?${q}` : ""}`);
  return r.json();
}

export async function getRecommendedItems(params?: {
  ta_id?: number;
  count?: number;
}): Promise<{ recommended: AssessmentItemDetail[]; solved_count: number }> {
  const sp = new URLSearchParams();
  if (params?.ta_id != null) sp.set("ta_id", String(params.ta_id));
  if (params?.count != null) sp.set("count", String(params.count));
  const q = sp.toString();
  const r = await apiFetch(`/assessment/recommend${q ? `?${q}` : ""}`);
  return r.json();
}

export async function getAssessmentStats(): Promise<AssessmentStats> {
  const r = await apiFetch("/assessment/stats");
  return r.json();
}

export async function getTeacherAssessmentOverview(): Promise<Record<string, unknown>> {
  const r = await apiFetch("/assessment/teacher/overview");
  return r.json();
}

// ---- Metrics Dashboard ----

export interface MetricsDashboardData {
  generated_at: string;
  totals: {
    total_items: number;
    evaluated_items: number;
    low_ai_items: number;
    avg_ai_pass_rate: number | null;
    total_attempts: number;
    correct_attempts: number;
    telemetry_events: number;
  };
  type_overview: {
    item_type: string;
    total_items: number;
    evaluated_items: number;
    low_ai_items: number;
    avg_ai_pass_rate: number | null;
  }[];
  ai_pass_distribution: {
    bucket: string;
    parsons: number;
    dropdown: number;
    execution_trace: number;
  }[];
  theme_overview: {
    theme: string;
    total_items: number;
    low_ai_items: number;
    avg_ai_pass_rate: number | null;
  }[];
  telemetry: {
    available: boolean;
    total_events: number;
    focus_loss_count: number;
    resume_count: number;
    event_breakdown: { event_type: string; count: number }[];
  };
}

export async function getMetricsDashboard(): Promise<MetricsDashboardData> {
  const r = await apiFetch("/assessment/metrics");
  return r.json();
}
