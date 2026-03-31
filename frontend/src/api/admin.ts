import { getToken } from "./client";

const API_BASE =
  import.meta.env.VITE_API_URL || (import.meta.env.DEV ? "/api" : "/api");

function authHeaders(): HeadersInit {
  const h: HeadersInit = { "Content-Type": "application/json" };
  const t = getToken();
  if (t) h["Authorization"] = `Bearer ${t}`;
  return h;
}

// ── Types ──────────────────────────────────────────────────────────

export interface AdminSettings {
  anti_capture_enabled: boolean;
  anti_capture_hz: number;
  focus_loss_threshold: number;
  min_solve_time_ms: number;
  typing_anomaly_enabled: boolean;
  watermark_enabled: boolean;
  devtools_detection_enabled: boolean;
  print_block_enabled: boolean;
  ocr_noise_enabled: boolean;
  [key: string]: unknown;
}

export interface StudentFlagItem {
  id: number;
  user_id: number;
  username: string | null;
  flag_type: string;
  severity: string;
  detail: Record<string, unknown> | null;
  session_id: string | null;
  item_id: number | null;
  resolved: boolean;
  resolved_by: number | null;
  resolved_at: string | null;
  created_at: string | null;
}

export interface FlagSummaryStudent {
  user_id: number;
  username: string;
  total_flags: number;
  unresolved: number;
  critical: number;
  warning: number;
  info: number;
  latest_flag_at: string | null;
}

// ── Config ─────────────────────────────────────────────────────────

export async function getAdminConfig(): Promise<AdminSettings> {
  const r = await fetch(`${API_BASE}/admin/config`, { headers: authHeaders() });
  const data = await r.json();
  return data.settings;
}

export async function updateAdminConfig(
  settings: Partial<AdminSettings>
): Promise<AdminSettings> {
  const r = await fetch(`${API_BASE}/admin/config`, {
    method: "PUT",
    headers: authHeaders(),
    body: JSON.stringify({ settings }),
  });
  if (!r.ok) throw new Error(await r.text());
  const data = await r.json();
  return data.settings;
}

// ── Flags ──────────────────────────────────────────────────────────

export async function getFlags(params?: {
  user_id?: number;
  flag_type?: string;
  severity?: string;
  resolved?: boolean;
  limit?: number;
  offset?: number;
}): Promise<{ flags: StudentFlagItem[]; total: number }> {
  const sp = new URLSearchParams();
  if (params?.user_id != null) sp.set("user_id", String(params.user_id));
  if (params?.flag_type) sp.set("flag_type", params.flag_type);
  if (params?.severity) sp.set("severity", params.severity);
  if (params?.resolved != null) sp.set("resolved", String(params.resolved));
  if (params?.limit != null) sp.set("limit", String(params.limit));
  if (params?.offset != null) sp.set("offset", String(params.offset));
  const q = sp.toString();
  const r = await fetch(`${API_BASE}/admin/flags${q ? `?${q}` : ""}`, {
    headers: authHeaders(),
  });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function createFlag(body: {
  user_id: number;
  flag_type: string;
  severity?: string;
  detail?: Record<string, unknown>;
  session_id?: string;
  item_id?: number;
}): Promise<{ id: number; ok: boolean }> {
  const r = await fetch(`${API_BASE}/admin/flags`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify(body),
  });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function resolveFlag(
  flagId: number
): Promise<{ ok: boolean }> {
  const r = await fetch(`${API_BASE}/admin/flags/${flagId}`, {
    method: "PATCH",
    headers: authHeaders(),
  });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function getFlagSummary(): Promise<{
  students: FlagSummaryStudent[];
}> {
  const r = await fetch(`${API_BASE}/admin/flags/summary`, {
    headers: authHeaders(),
  });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}
