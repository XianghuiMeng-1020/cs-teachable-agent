# Assessment Studio

`assessment-studio/` is now a student-facing Parsons practice interface built on top of real PyTaskSyn outputs in this repository.

## What it does now

- reads real `outputs/query_*` artifacts through Next.js API routes
- only surfaces Parsons items whose measured AI pass rate is below the chosen threshold
- lets a student-like user select blocks, order them, submit, and get feedback
- keeps the answer key on the server side through a grading route
- tracks local attempt progress in the browser session

## Run

```bash
cd assessment-studio
npm install
npm run dev
```

Open `http://localhost:3000`.

### Optional: point hints to an external backend

If OpenAI is blocked in your local or deployed Next.js server environment, you can keep this frontend where it is and send only hint requests to a separate backend:

```bash
export NEXT_PUBLIC_HINT_API_BASE_URL="https://your-hint-backend.example.com"
```

The page will then call:

```text
https://your-hint-backend.example.com/student/hint
```

If this variable is not set, hints use the built-in route:

```text
/api/studio/student/hint
```

The standalone service is in [hint-backend/README.md](/Volumes/T7/idea/pytasksyn/hint-backend/README.md).

### Developer-only browser key mode

In local `npm run dev`, the hint panel also exposes a `Developer only` section. You can paste a temporary OpenAI API key there and switch the panel to `Browser direct mode`.

Constraints:

- the key is stored only in React state for the current tab
- the key is cleared on refresh
- this is for local development only
- do not use this mode in public deployments

## Student API routes

- `/api/studio/student/index`: eligible Parsons items under the selected AI-pass threshold
- `/api/studio/student/task`: student-safe task content without the answer key
- `/api/studio/student/grade`: server-side grading for a submitted Parsons answer

## Deploy To Hugging Face

Do not upload the repository root directly. The root contains research artifacts, local build outputs, and dependencies that are not needed for the student-facing app.

Instead, build a minimal Hugging Face Space bundle from the repository root:

```bash
python3 scripts/build_hf_space_bundle.py
```

This creates `hf-space/` with:

- the Next.js frontend source from `assessment-studio/`
- only the typed assessment JSON files and evaluation summaries needed by the student app
- a Docker-based Hugging Face Space configuration

Then upload that bundle to a Space repo, not a model repo:

```bash
python3 scripts/upload_hf_space.py --repo-id YOUR_NAME/YOUR_SPACE_NAME
```

If you prefer the raw Python API, the important part is `repo_type="space"` instead of `repo_type="model"`.
