export interface User {
  id: number;
  username: string;
  role: "student" | "teacher";
}

export interface TAInstance {
  id: number;
  domain_id: string;
  name?: string;
  user_id?: number;
}

export interface KnowledgeUnitState {
  unit_id: string;
  status: "unknown" | "partially_learned" | "learned" | "misconception" | "corrected";
}

export interface TeachEvent {
  student_input: string;
  topic_taught?: string;
  interpreted_units?: string[];
  quality_score?: number;
  ta_response: string;
  timestamp?: string;
}

export interface TestAttempt {
  problem_id: string;
  problem_statement: string;
  ta_code: string;
  passed: boolean;
  details: { input: string; expected: string; got: string; passed: boolean }[];
  mastery_report?: Record<string, unknown>;
}

export interface TAState {
  knowledge_units: KnowledgeUnitState[];
  active_misconceptions: string[];
  overall_mastery_summary?: string;
}

export interface HistoryEvent {
  id: string;
  type: "teach" | "test_pass" | "test_fail" | "misconception_activated" | "correction" | "relearning";
  title: string;
  description: string;
  timestamp: string;
  metadata?: Record<string, unknown>;
}

export interface TranscriptSession {
  session_id: number;
  student: { id: number; username: string };
  ta_id: number;
  domain_id: string;
  message_count: number;
  kus_covered: string[];
  started_at: string;
  ended_at?: string;
}

export interface TranscriptMessage {
  seq: number;
  type: "teach" | "test";
  speaker: "student" | "ta" | "system";
  content: string;
  interpreted_units: string[] | null;
  quality_score: number | null;
  timestamp: string;
}

export interface MisconceptionDetail {
  id: string;
  description: string;
  affected_units: string[];
  remediation_hint: string;
  status: "active" | "correcting" | "resolved";
  activated_at?: string;
}
