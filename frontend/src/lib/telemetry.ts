import { getToken } from "@/api/client";

export type TelemetryEventType =
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
  | "hint_escalation_saved"
  | "paste_blocked"
  | "typing_anomaly"
  | "content_copied"
  | "devtools_opened";

export interface TelemetryEvent {
  eventType: TelemetryEventType;
  sessionId: string;
  attemptId?: string;
  itemId?: number;
  itemType?: string;
  payload?: Record<string, unknown>;
  eventTime?: string;
}

const API_BASE = import.meta.env.VITE_API_URL
  || (import.meta.env.DEV ? "/api" : "/api");

let _sessionId: string | null = null;

export function getSessionId(): string {
  if (!_sessionId) {
    _sessionId = `sess_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
  }
  return _sessionId;
}

export function generateAttemptId(): string {
  return `att_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
}

export function emitTelemetry(
  eventType: TelemetryEventType,
  payload?: Record<string, unknown>,
  context?: { itemId?: number; itemType?: string; attemptId?: string; eventTime?: string }
) {
  const event: TelemetryEvent = {
    eventType,
    sessionId: getSessionId(),
    attemptId: context?.attemptId,
    itemId: context?.itemId,
    itemType: context?.itemType,
    payload,
    eventTime: context?.eventTime ?? new Date().toISOString(),
  };

  const token = getToken();
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  try {
    fetch(`${API_BASE}/assessment/telemetry`, {
      method: "POST",
      headers,
      body: JSON.stringify(event),
    }).catch(() => {});
  } catch {
    // fire and forget
  }
}

export function emitTelemetryBeacon(
  eventType: TelemetryEventType,
  payload?: Record<string, unknown>
) {
  const event: TelemetryEvent = {
    eventType,
    sessionId: getSessionId(),
    payload,
    eventTime: new Date().toISOString(),
  };

  try {
    const blob = new Blob([JSON.stringify(event)], { type: "application/json" });
    navigator.sendBeacon(`${API_BASE}/assessment/telemetry`, blob);
  } catch {
    // fallback
    emitTelemetry(eventType, payload);
  }
}

export function setupSessionTelemetry() {
  emitTelemetry("session_started", {
    userAgent: navigator.userAgent,
    viewport: `${window.innerWidth}x${window.innerHeight}`,
  });

  const handleUnload = () => {
    emitTelemetryBeacon("session_ended");
  };

  window.addEventListener("beforeunload", handleUnload);
  return () => window.removeEventListener("beforeunload", handleUnload);
}
