import { randomUUID } from "node:crypto";

const OPENAI_HINT_MODEL = process.env.OPENAI_HINT_MODEL?.trim() || "gpt-4o-mini";

const STUDENT_HINT_RESPONSE_SCHEMA = {
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
};

export async function generateStudentHint(request) {
  if (!process.env.OPENAI_API_KEY) {
    throw new Error("OPENAI_API_KEY is not configured.");
  }

  const task = request?.taskContext;
  if (!task || typeof task !== "object") {
    throw new Error("taskContext is required for the standalone hint backend.");
  }

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
    body: JSON.stringify({
      model: OPENAI_HINT_MODEL,
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
          schema: STUDENT_HINT_RESPONSE_SCHEMA,
          strict: true
        }
      }
    })
  });

  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload?.error?.message ?? "OpenAI hint generation failed.");
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

function buildSystemPrompt() {
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

function buildHintPromptPayload(task, request) {
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

function buildFeedbackSnapshot(feedback) {
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

function buildTaskSnapshot(task) {
  if (task.itemType === "parsons") {
    return {
      itemType: task.itemType,
      title: task.title,
      prompt: clipText(task.prompt, 900),
      theme: task.theme,
      concepts: Array.isArray(task.concepts) ? task.concepts : [],
      requiredBlockCount: task.requiredBlockCount,
      optionPool: Array.isArray(task.options)
        ? task.options.map((option, index) => ({
            blockId: `block_${index + 1}`,
            text: clipText(String(option), 180)
          }))
        : []
    };
  }

  if (task.itemType === "dropdown") {
    return {
      itemType: task.itemType,
      title: task.title,
      prompt: clipText(task.prompt, 900),
      theme: task.theme,
      concepts: Array.isArray(task.concepts) ? task.concepts : [],
      promptTemplate: clipText(task.promptTemplate, 1200),
      blanks: Array.isArray(task.blanks)
        ? task.blanks.map((blank) => ({
            blankId: blank.blankId,
            placeholder: blank.placeholder,
            options: Array.isArray(blank.options) ? blank.options.map((option) => clipText(String(option), 120)) : []
          }))
        : []
    };
  }

  return {
    itemType: task.itemType,
    title: task.title,
    prompt: clipText(task.prompt, 900),
    theme: task.theme,
    concepts: Array.isArray(task.concepts) ? task.concepts : [],
    functionName: task.functionName,
    callExpression: clipText(task.callExpression, 240),
    functionSource: clipText(task.functionSource, 1800),
    checkpoints: Array.isArray(task.checkpoints)
      ? task.checkpoints.map((checkpoint) => ({
          checkpointId: checkpoint.checkpointId,
          lineNumber: checkpoint.lineNumber,
          lineExcerpt: clipText(checkpoint.lineExcerpt, 180),
          variableName: checkpoint.variableName
        }))
      : []
  };
}

function buildSubmissionSnapshot(task, request) {
  if (task.itemType === "parsons") {
    const selectedBlocks = Array.isArray(request.selectedBlocks) ? request.selectedBlocks : [];
    return {
      itemType: task.itemType,
      selectedCount: selectedBlocks.length,
      requiredCount: task.requiredBlockCount,
      selectedBlocks: selectedBlocks.map((block, index) => ({
        position: index + 1,
        text: clipText(String(block), 180)
      })),
      unplacedCount: Math.max(task.requiredBlockCount - selectedBlocks.length, 0)
    };
  }

  const selectedAnswers =
    request.selectedAnswers && typeof request.selectedAnswers === "object" ? request.selectedAnswers : {};

  if (task.itemType === "dropdown") {
    return {
      itemType: task.itemType,
      answeredCount: Array.isArray(task.blanks)
        ? task.blanks.filter((blank) => normalizeOptionalText(selectedAnswers[blank.blankId])).length
        : 0,
      requiredCount: task.requiredBlankCount,
      selectedAnswers: Array.isArray(task.blanks)
        ? task.blanks.map((blank) => ({
            blankId: blank.blankId,
            placeholder: blank.placeholder,
            selected: normalizeOptionalText(selectedAnswers[blank.blankId])
          }))
        : []
    };
  }

  return {
    itemType: task.itemType,
    answeredCount: Array.isArray(task.checkpoints)
      ? task.checkpoints.filter((checkpoint) => normalizeOptionalText(selectedAnswers[checkpoint.checkpointId])).length
      : 0,
    requiredCount: task.requiredCheckpointCount,
    selectedAnswers: Array.isArray(task.checkpoints)
      ? task.checkpoints.map((checkpoint) => ({
          checkpointId: checkpoint.checkpointId,
          variableName: checkpoint.variableName,
          lineNumber: checkpoint.lineNumber,
          selected: normalizeOptionalText(selectedAnswers[checkpoint.checkpointId])
        }))
      : []
  };
}

function parseHintModelOutput(payload) {
  const rawText = extractResponseText(payload);
  if (!rawText) {
    throw new Error("OpenAI returned an empty hint response.");
  }

  const parsed = JSON.parse(rawText);
  return {
    title: typeof parsed.title === "string" ? parsed.title : "",
    body: typeof parsed.body === "string" ? parsed.body : "",
    target: parseTarget(parsed.target),
    escalationAvailable: parsed.escalationAvailable !== false
  };
}

function extractResponseText(payload) {
  if (typeof payload?.output_text === "string" && payload.output_text.trim().length > 0) {
    return payload.output_text.trim();
  }

  const parts =
    payload?.output?.flatMap((item) =>
      (item.content ?? [])
        .map((content) => (typeof content.text === "string" ? content.text : ""))
        .filter((text) => text.trim().length > 0)
    ) ?? [];

  return parts.join("\n").trim();
}

function parseTarget(value) {
  if (!value || typeof value !== "object") {
    return null;
  }

  const kind = value.kind;
  const id = value.id;
  const label = value.label;
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

function normalizeHintTitle(title, hintType, level) {
  const cleaned = typeof title === "string" ? title.replace(/\s+/g, " ").trim() : "";
  if (cleaned.length > 0) {
    return clipText(cleaned, 72);
  }

  const fallbackPrefix =
    hintType === "understand" ? "Task frame" : hintType === "next-step" ? "Next move" : "Issue check";
  return `${fallbackPrefix} · Level ${level}`;
}

function normalizeHintBody(body) {
  const cleaned = typeof body === "string" ? body.replace(/\s+/g, " ").trim() : "";
  if (cleaned.length === 0) {
    throw new Error("OpenAI returned an empty hint body.");
  }
  return clipText(cleaned, 420);
}

function normalizeHintTarget(target) {
  if (!target) {
    return null;
  }

  return {
    kind: target.kind,
    id: clipText(target.id, 80),
    label: clipText(target.label, 80)
  };
}

function normalizeOptionalText(value) {
  return typeof value === "string" && value.trim().length > 0 ? clipText(value.trim(), 240) : null;
}

function clipText(value, maxLength) {
  const normalized = String(value).replace(/\s+/g, " ").trim();
  return normalized.length <= maxLength ? normalized : `${normalized.slice(0, maxLength - 3)}...`;
}
