import { createServer } from "node:http";
import { generateStudentHint } from "./hint-service.mjs";

const PORT = Number.parseInt(process.env.PORT ?? "8787", 10);
const MAX_BODY_BYTES = 1_000_000;
const ALLOWED_ORIGINS = parseAllowedOrigins(process.env.ALLOWED_ORIGINS ?? "*");

const server = createServer(async (request, response) => {
  const origin = request.headers.origin;
  const allowedOrigin = resolveAllowedOrigin(origin);

  applyCors(response, allowedOrigin);

  if (request.method === "OPTIONS") {
    response.writeHead(204);
    response.end();
    return;
  }

  if (request.method === "GET" && request.url === "/health") {
    sendJson(response, 200, {
      ok: true,
      model: process.env.OPENAI_HINT_MODEL?.trim() || "gpt-4o-mini"
    });
    return;
  }

  if (request.method === "POST" && request.url === "/student/hint") {
    if (origin && !allowedOrigin) {
      sendJson(response, 403, { error: "Origin not allowed." });
      return;
    }

    try {
      const body = await readJsonBody(request);
      const validationError = validateHintRequest(body);
      if (validationError) {
        sendJson(response, 400, { error: validationError });
        return;
      }

      const hint = await generateStudentHint(body);
      sendJson(response, 200, hint);
    } catch (error) {
      sendJson(response, 500, {
        error: error instanceof Error ? error.message : "Failed to generate hint."
      });
    }
    return;
  }

  sendJson(response, 404, { error: "Not found." });
});

server.listen(PORT, () => {
  process.stdout.write(`hint-backend listening on http://0.0.0.0:${PORT}\n`);
});

function applyCors(response, allowedOrigin) {
  if (allowedOrigin) {
    response.setHeader("Access-Control-Allow-Origin", allowedOrigin);
  }
  response.setHeader("Access-Control-Allow-Methods", "GET,POST,OPTIONS");
  response.setHeader("Access-Control-Allow-Headers", "Content-Type");
  response.setHeader("Vary", "Origin");
}

function sendJson(response, statusCode, payload) {
  response.writeHead(statusCode, {
    "Content-Type": "application/json; charset=utf-8"
  });
  response.end(JSON.stringify(payload));
}

function parseAllowedOrigins(rawValue) {
  const normalized = rawValue.trim();
  if (!normalized || normalized === "*") {
    return "*";
  }

  return normalized
    .split(",")
    .map((value) => value.trim())
    .filter((value) => value.length > 0);
}

function resolveAllowedOrigin(origin) {
  if (ALLOWED_ORIGINS === "*") {
    return "*";
  }

  if (!origin) {
    return null;
  }

  return ALLOWED_ORIGINS.includes(origin) ? origin : null;
}

async function readJsonBody(request) {
  const chunks = [];
  let totalBytes = 0;

  for await (const chunk of request) {
    totalBytes += chunk.length;
    if (totalBytes > MAX_BODY_BYTES) {
      throw new Error("Request body is too large.");
    }
    chunks.push(chunk);
  }

  const text = Buffer.concat(chunks).toString("utf8");
  if (!text) {
    throw new Error("Request body is empty.");
  }

  return JSON.parse(text);
}

function validateHintRequest(body) {
  if (!body || typeof body !== "object") {
    return "JSON body is required.";
  }

  if (!body.queryId || !body.taskId || !body.itemType || !body.hintType || !body.level) {
    return "queryId, taskId, itemType, hintType, and level are required.";
  }

  if (body.itemType !== "parsons" && body.itemType !== "dropdown" && body.itemType !== "execution-trace") {
    return "Unsupported itemType.";
  }

  if (
    body.hintType !== "understand" &&
    body.hintType !== "next-step" &&
    body.hintType !== "check-one-issue"
  ) {
    return "Unsupported hintType.";
  }

  if (body.level !== 1 && body.level !== 2 && body.level !== 3) {
    return "level must be 1, 2, or 3.";
  }

  if (!body.taskContext || typeof body.taskContext !== "object") {
    return "taskContext is required.";
  }

  if (body.taskContext.itemType !== body.itemType) {
    return "taskContext.itemType must match itemType.";
  }

  return null;
}
