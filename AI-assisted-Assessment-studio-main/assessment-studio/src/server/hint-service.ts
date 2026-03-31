import { randomUUID } from "node:crypto";
import {
  buildOpenAIHintRequestBody,
  DEFAULT_OPENAI_HINT_MODEL,
  normalizeHintBody,
  normalizeHintTarget,
  normalizeHintTitle,
  parseHintModelOutput,
  type OpenAIResponsesPayload
} from "@/src/hints/openai-hint";
import { getStudentTask } from "@/src/server/studio-data";
import type {
  StudentHintRequest,
  StudentHintResponse
} from "@/src/types";

const OPENAI_HINT_MODEL = process.env.OPENAI_HINT_MODEL?.trim() || DEFAULT_OPENAI_HINT_MODEL;

export async function generateStudentHint(request: StudentHintRequest): Promise<StudentHintResponse> {
  if (!process.env.OPENAI_API_KEY) {
    throw new Error("OPENAI_API_KEY is not available in the Next.js server environment.");
  }

  const task = request.taskContext ?? (await getStudentTask(request.queryId, request.taskId, request.itemType));

  if (request.lastFeedback?.correct) {
    return {
      hintId: `hint-${randomUUID()}`,
      hintType: request.hintType,
      level: request.level,
      title: "Already solved",
      body: "This attempt is already correct. Use the feedback to confirm why it works, or move to the next task.",
      target: null,
      escalationAvailable: false,
      model: "local-status"
    };
  }

  const response = await fetch("https://api.openai.com/v1/responses", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${process.env.OPENAI_API_KEY}`
    },
    body: JSON.stringify(buildOpenAIHintRequestBody(task, request, OPENAI_HINT_MODEL))
  });

  const payload = (await response.json()) as OpenAIResponsesPayload;
  if (!response.ok) {
    throw new Error(payload.error?.message ?? "OpenAI hint generation failed.");
  }

  const parsed = parseHintModelOutput(payload);
  return {
    hintId: `hint-${randomUUID()}`,
    hintType: request.hintType,
    level: request.level,
    title: normalizeHintTitle(parsed.title, request.hintType, request.level),
    body: normalizeHintBody(parsed.body),
    target: normalizeHintTarget(parsed.target),
    escalationAvailable: parsed.escalationAvailable,
    model: OPENAI_HINT_MODEL
  };
}
