# Hint Backend

`hint-backend/` is a standalone Node service for AI hints. It exists so the student frontend can stay where it is, while the OpenAI call is moved to a separate server in a supported region.

## What it does

- exposes `POST /student/hint`
- accepts the current task context from the browser
- calls OpenAI `responses` on the server side
- returns one short structured hint
- supports browser CORS through `ALLOWED_ORIGINS`

## Run locally

```bash
cd hint-backend
cp .env.example .env
export $(grep -v '^#' .env | xargs)
npm start
```

Health check:

```bash
curl http://localhost:8787/health
```

## Required environment variables

- `OPENAI_API_KEY`
- `OPENAI_HINT_MODEL` optional, defaults to `gpt-4o-mini`
- `PORT` optional, defaults to `8787`
- `ALLOWED_ORIGINS` comma-separated browser origins allowed to call this API

Example:

```bash
ALLOWED_ORIGINS=http://localhost:3000,https://your-space-domain.hf.space
```

## Connect the frontend

In `assessment-studio`, point the client to this backend:

```bash
export NEXT_PUBLIC_HINT_API_BASE_URL="https://your-hint-backend.example.com"
```

When this variable is set, the student page sends hint requests to:

```text
https://your-hint-backend.example.com/student/hint
```

If the variable is not set, the frontend falls back to its built-in Next.js route:

```text
/api/studio/student/hint
```

## Deployment shape

Deploy this folder to any Node host located in an OpenAI-supported region. The frontend does not need to move; only this backend needs to run in that region.
