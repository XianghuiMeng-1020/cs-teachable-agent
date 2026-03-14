# Demo Script — CS Teachable Agent

Use this script to demonstrate the full **teach → test → reflect** loop to your teacher or stakeholders.

## Prerequisites

1. **Backend**: From repo root run `uvicorn src.api.main:app --reload --host 127.0.0.1 --port 8000`
2. **Frontend**: `cd frontend && npm install && npm run dev` (serves at http://localhost:3000)
3. Or use Docker: `docker-compose up backend` then run frontend locally with proxy to `/api` → `http://127.0.0.1:8000`

## Demo Steps

### 1. Login / Register

- Open http://localhost:3000
- Register a new user (e.g. username: `demo`, password: `demo`)
- You are taken to the Student page

### 2. Create or select a TA

- If no TA exists, one is created automatically (Python domain)
- You can create more TAs via the dropdown (create from API if needed)

### 3. Teach the TA (Chat panel)

- In the **Chat** panel (left), type a short teaching message, for example:
  - *"A variable is like a box. You put a value in it with equals. For example: x = 5. Then you can print it with print(x)."*
- Click **Send**
- The TA replies as a learner (e.g. "So x = 5 means the variable stores the value 5?")
- The **State** panel (right) updates: **Learned units** should include e.g. `variable_assignment`, `print_function`

### 4. Run a test (Workspace panel)

- Switch to **Test** mode in the center **Workspace**
- Click **Run test**
- The system selects a problem that only uses concepts the TA has learned
- You see:
  - **Problem** description
  - **TA code** (generated or stub)
  - **PASS** or **FAIL**
  - **Mastery** summary

### 5. Reflect (optional)

- If the TA **failed**, point out: "The student can see the TA's wrong code and think about what to re-teach."
- If the TA **passed**, point out: "The TA only used what was taught; the state constrained its behavior."

### 6. Teacher dashboard (optional)

- Log in as a user with `role: teacher` (create via API or DB)
- Open **Teacher Dashboard** from the login page link
- Show **Students** list and **Class overview**

## API-only demo (no frontend)

```bash
# Register
curl -X POST http://127.0.0.1:8000/api/auth/register -H "Content-Type: application/json" -d "{\"username\":\"demo\",\"password\":\"demo\",\"role\":\"student\"}"

# Login
curl -X POST http://127.0.0.1:8000/api/auth/login -H "Content-Type: application/json" -d "{\"username\":\"demo\",\"password\":\"demo\"}"
# Save the access_token from response.

# Create TA (use token)
curl -X POST http://127.0.0.1:8000/api/ta -H "Authorization: Bearer YOUR_TOKEN" -H "Content-Type: application/json" -d "{\"domain_id\":\"python\"}"

# Teach (use token and ta_id from previous response)
curl -X POST http://127.0.0.1:8000/api/ta/1/teach -H "Authorization: Bearer YOUR_TOKEN" -H "Content-Type: application/json" -d "{\"student_input\":\"Variables store values. x = 5 and print(x).\"}"

# Test
curl -X POST http://127.0.0.1:8000/api/ta/1/test -H "Authorization: Bearer YOUR_TOKEN" -H "Content-Type: application/json" -d "{}"
```

## Talking points

- **Zero knowledge**: The TA starts with no Python knowledge; only taught concepts appear in state.
- **Knowledge state constraint**: TA dialogue and code are driven by the structured state, not raw LLM.
- **Two channels**: Teaching (conversation) + Testing (programming problems) together support learning-by-teaching.
- **Misconceptions**: The system can model misconceptions (e.g. assign_vs_equal); correction and relearning are in the core design.
