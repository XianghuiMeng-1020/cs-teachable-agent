import type {
  StudentGradeResponse,
  StudentHintRequest,
  StudentHintTarget,
  StudentHintType,
  StudentTaskResponse
} from "@/src/types";

export const DEFAULT_OPENAI_HINT_MODEL = "gpt-4o-mini";

export const OPENAI_HINT_RESPONSE_SCHEMA = {
  type: "object",
  additionalProperties: false,
  required: ["title", "body", "target", "escalationAvailable"],
  properties: {
    title: { type: "string" },
    body: { type: "string" },
    target: {
      anyOf: [
        { type: "null" },
        {
          type: "object",
          additionalProperties: false,
          required: ["kind", "id", "label"],
          properties: {
            kind: {
              type: "string",
              enum: ["blank", "checkpoint", "block", "task"]
            },
            id: { type: "string" },
            label: { type: "string" }
          }
        }
      ]
    },
    escalationAvailable: { type: "boolean" }
  }
} as const;

export type OpenAIResponsesPayload = {
  output_text?: string;
  output?: Array<{
    content?: Array<{
      type?: string;
      text?: string;
    }>;
  }>;
  error?: {
    message?: string;
  };
};

export type ParsedHintModelOutput = {
  title: string;
  body: string;
  target: StudentHintTarget;
  escalationAvailable: boolean;
};

export function buildOpenAIHintRequestBody(
  task: StudentTaskResponse,
  request: StudentHintRequest,
  model: string
) {
  return {
    model,
    input: [
      {
        role: "system",
        content: [
          {
            type: "input_text",
            text: buildSystemPrompt()
          }
        ]
      },
      {
        role: "user",
        content: [
          {
            type: "input_text",
            text: JSON.stringify(buildHintPromptPayload(task, request), null, 2)
          }
        ]
      }
    ],
    text: {
      format: {
        type: "json_schema",
        name: "student_hint",
        schema: OPENAI_HINT_RESPONSE_SCHEMA,
        strict: true
      }
    }
  };
}

export function parseHintModelOutput(payload: OpenAIResponsesPayload): ParsedHintModelOutput {
  const rawText = extractResponseText(payload);
  if (!rawText) {
    throw new Error("OpenAI returned an empty hint response.");
  }

  const parsed = JSON.parse(rawText) as {
    title?: unknown;
    body?: unknown;
    target?: unknown;
    escalationAvailable?: unknown;
  };

  return {
    title: typeof parsed.title === "string" ? parsed.title : "",
    body: typeof parsed.body === "string" ? parsed.body : "",
    target: parseTarget(parsed.target),
    escalationAvailable: parsed.escalationAvailable !== false
  };
}

export function normalizeHintTitle(title: string, hintType: StudentHintType, level: 1 | 2 | 3): string {
  const cleaned = title.replace(/\s+/g, " ").trim();
  if (cleaned.length > 0) {
    return clipText(cleaned, 72);
  }

  const fallbackPrefix =
    hintType === "understand"
      ? "Task frame"
      : hintType === "next-step"
        ? "Next move"
        : "Issue check";
  return `${fallbackPrefix} · Level ${level}`;
}

export function normalizeHintBody(body: string): string {
  const cleaned = body.replace(/\s+/g, " ").trim();
  if (cleaned.length === 0) {
    throw new Error("OpenAI returned an empty hint body.");
  }
  return clipText(cleaned, 420);
}

export function normalizeHintTarget(target: StudentHintTarget): StudentHintTarget {
  if (!target) {
    return null;
  }

  return {
    kind: target.kind,
    id: clipText(target.id, 80),
    label: clipText(target.label, 80)
  };
}

function buildSystemPrompt(): string {
  return [
    "You are a concise programming coach inside a structured student practice UI.",
    "Write one short hint that helps the student make the next move without revealing the full answer.",
    "Rules:",
    "- Keep the body to at most 2 sentences and under 60 words.",
    "- Never give the exact final block order, the exact dropdown option to pick, or the exact checkpoint values.",
    "- Level 1 should stay broad, level 2 can point to a local area, and level 3 can name one target area without giving the answer away.",
    "- If hintType is understand, explain what the student is trying to accomplish.",
    "- If hintType is next-step, suggest the next concrete action.",
    "- If hintType is check-one-issue, identify one likely issue to inspect.",
    "- Prefer actionable wording over theory.",
    "- If the student already has some correct progress, build on that instead of restarting the whole task."
  ].join("\n");
}

function buildHintPromptPayload(task: StudentTaskResponse, request: StudentHintRequest) {
  return {
    requested_help: {
      hintType: request.hintType,
      level: request.level,
      reflection: normalizeOptionalText(request.reflection),
      progressSummary: normalizeOptionalText(request.progressSummary),
      attemptNumber: request.attemptNumber ?? null
    },
    latest_feedback: buildFeedbackSnapshot(request.lastFeedback ?? null),
    task: buildTaskSnapshot(task),
    current_submission: buildSubmissionSnapshot(task, request)
  };
}

function buildFeedbackSnapshot(feedback: StudentGradeResponse | null) {
  if (!feedback) {
    return null;
  }

  return {
    correct: feedback.correct,
    feedback: clipText(feedback.feedback, 220),
    expectedCount: feedback.expectedCount,
    selectedCount: feedback.selectedCount,
    correctCount: feedback.correctCount
  };
}

function buildTaskSnapshot(task: StudentTaskResponse) {
  if (task.itemType === "parsons") {
    return {
      itemType: task.itemType,
      title: task.title,
      prompt: clipText(task.prompt, 900),
      theme: task.theme,
      concepts: task.concepts,
      requiredBlockCount: task.requiredBlockCount,
      optionPool: task.options.map((option, index) => ({
        blockId: `block_${index + 1}`,
        text: clipText(option, 180)
      }))
    };
  }

  if (task.itemType === "dropdown") {
    return {
      itemType: task.itemType,
      title: task.title,
      prompt: clipText(task.prompt, 900),
      theme: task.theme,
      concepts: task.concepts,
      promptTemplate: clipText(task.promptTemplate, 1200),
      blanks: task.blanks.map((blank) => ({
        blankId: blank.blankId,
        placeholder: blank.placeholder,
        options: blank.options.map((option) => clipText(option, 120))
      }))
    };
  }

  return {
    itemType: task.itemType,
    title: task.title,
    prompt: clipText(task.prompt, 900),
    theme: task.theme,
    concepts: task.concepts,
    functionName: task.functionName,
    callExpression: clipText(task.callExpression, 240),
    functionSource: clipText(task.functionSource, 1800),
    checkpoints: task.checkpoints.map((checkpoint) => ({
      checkpointId: checkpoint.checkpointId,
      lineNumber: checkpoint.lineNumber,
      lineExcerpt: clipText(checkpoint.lineExcerpt, 180),
      variableName: checkpoint.variableName
    }))
  };
}

function buildSubmissionSnapshot(task: StudentTaskResponse, request: StudentHintRequest) {
  if (task.itemType === "parsons") {
    const selectedBlocks = Array.isArray(request.selectedBlocks)
      ? request.selectedBlocks
      : [];

    return {
      itemType: task.itemType,
      selectedCount: selectedBlocks.length,
      requiredCount: task.requiredBlockCount,
      selectedBlocks: selectedBlocks.map((block, index) => ({
        position: index + 1,
        text: clipText(block, 180)
      })),
      unplacedCount: Math.max(task.requiredBlockCount - selectedBlocks.length, 0)
    };
  }

  const selectedAnswers =
    request.selectedAnswers && typeof request.selectedAnswers === "object"
      ? request.selectedAnswers
      : {};

  if (task.itemType === "dropdown") {
    return {
      itemType: task.itemType,
      answeredCount: task.blanks.filter((blank) => normalizeOptionalText(selectedAnswers[blank.blankId])).length,
      requiredCount: task.requiredBlankCount,
      selectedAnswers: task.blanks.map((blank) => ({
        blankId: blank.blankId,
        placeholder: blank.placeholder,
        selected: normalizeOptionalText(selectedAnswers[blank.blankId])
      }))
    };
  }

  return {
    itemType: task.itemType,
    answeredCount: task.checkpoints.filter((checkpoint) => normalizeOptionalText(selectedAnswers[checkpoint.checkpointId])).length,
    requiredCount: task.requiredCheckpointCount,
    selectedAnswers: task.checkpoints.map((checkpoint) => ({
      checkpointId: checkpoint.checkpointId,
      variableName: checkpoint.variableName,
      lineNumber: checkpoint.lineNumber,
      selected: normalizeOptionalText(selectedAnswers[checkpoint.checkpointId])
    }))
  };
}

function extractResponseText(payload: OpenAIResponsesPayload): string {
  if (typeof payload.output_text === "string" && payload.output_text.trim().length > 0) {
    return payload.output_text.trim();
  }

  const parts =
    payload.output?.flatMap((item) =>
      (item.content ?? [])
        .map((content) => (typeof content.text === "string" ? content.text : ""))
        .filter((text) => text.trim().length > 0)
    ) ?? [];

  return parts.join("\n").trim();
}

function parseTarget(value: unknown): StudentHintTarget {
  if (!value || typeof value !== "object") {
    return null;
  }

  const raw = value as Record<string, unknown>;
  const kind = raw.kind;
  const id = raw.id;
  const label = raw.label;
  if (
    (kind === "blank" || kind === "checkpoint" || kind === "block" || kind === "task") &&
    typeof id === "string" &&
    id.trim().length > 0
  ) {
    return {
      kind,
      id: id.trim(),
      label: typeof label === "string" && label.trim().length > 0 ? label.trim() : id.trim()
    };
  }

  return null;
}

function normalizeOptionalText(value: unknown): string | null {
  return typeof value === "string" && value.trim().length > 0 ? clipText(value.trim(), 240) : null;
}

function clipText(value: string, maxLength: number): string {
  const normalized = value.replace(/\s+/g, " ").trim();
  return normalized.length <= maxLength ? normalized : `${normalized.slice(0, maxLength - 3)}...`;
}
