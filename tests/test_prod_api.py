"""测试生产环境后端 API 的完整学生流程"""
import requests, sys, json

BASE = "https://cs-teachable-agent-production.up.railway.app/api"
USER = "prod_test_student_2026"
PASS = "testpass123"

def p(label, r):
    status = "OK" if r.status_code == 200 else f"FAIL({r.status_code})"
    body = r.text[:300]
    print(f"  {label}: {status} => {body}")
    return r

def main():
    s = requests.Session()
    s.headers["Content-Type"] = "application/json"
    fails = []

    print("=== 生产环境后端 API 测试 ===\n")

    # 1. Health
    r = p("1. Health", s.get(f"{BASE}/health", timeout=15))
    if r.status_code != 200: fails.append("health")

    # 2. Config
    r = p("2. Config", s.get(f"{BASE}/config", timeout=15))
    if r.status_code != 200: fails.append("config")

    # 3. Register
    r = s.post(f"{BASE}/auth/register", json={"username": USER, "password": PASS, "role": "student"}, timeout=15)
    if r.status_code == 200:
        p("3. Register", r)
    elif "already registered" in r.text.lower():
        print(f"  3. Register: user exists (OK)")
    else:
        p("3. Register", r)
        fails.append("register")

    # 4. Login
    r = p("4. Login", s.post(f"{BASE}/auth/login", json={"username": USER, "password": PASS}, timeout=15))
    if r.status_code != 200:
        fails.append("login")
        print(f"\n  Cannot continue without login. Fails: {fails}")
        return 1
    token = r.json()["access_token"]
    s.headers["Authorization"] = f"Bearer {token}"

    # 5. Me
    r = p("5. Me", s.get(f"{BASE}/auth/me", timeout=15))
    if r.status_code != 200: fails.append("me")

    # 6. List TA
    r = p("6. List TA", s.get(f"{BASE}/ta", timeout=15))
    if r.status_code != 200: fails.append("list_ta")
    tas = r.json() if r.status_code == 200 else []

    # 7. Create TA
    r = p("7. Create TA", s.post(f"{BASE}/ta", json={"domain_id": "python", "name": "ProdTest"}, timeout=15))
    if r.status_code != 200:
        fails.append("create_ta")
        if tas:
            ta_id = tas[0]["id"]
            print(f"     Using existing TA #{ta_id}")
        else:
            print(f"\n  No TA available. Fails: {fails}")
            return 1
    else:
        ta_id = r.json()["id"]

    # 8. Teach
    r = p("8. Teach", s.post(f"{BASE}/ta/{ta_id}/teach", json={"student_input": "A variable stores a value. Use = to assign, like x = 5."}, timeout=30))
    if r.status_code != 200: fails.append("teach")

    # 9. State
    r = p("9. State", s.get(f"{BASE}/ta/{ta_id}/state", timeout=15))
    if r.status_code != 200: fails.append("state")

    # 10. Problems
    r = p("10. Problems", s.get(f"{BASE}/ta/{ta_id}/problems", timeout=15))
    if r.status_code != 200: fails.append("problems")

    # 11. Test
    r = p("11. Test", s.post(f"{BASE}/ta/{ta_id}/test", json={}, timeout=30))
    if r.status_code != 200: fails.append("test")

    # 12. Mastery
    r = p("12. Mastery", s.get(f"{BASE}/ta/{ta_id}/mastery", timeout=15))
    if r.status_code != 200: fails.append("mastery")

    # 13. Misconceptions
    r = p("13. Misconceptions", s.get(f"{BASE}/ta/{ta_id}/misconceptions", timeout=15))
    if r.status_code != 200: fails.append("misconceptions")

    # 14. History
    r = p("14. History", s.get(f"{BASE}/ta/{ta_id}/history?page=1&per_page=5", timeout=15))
    if r.status_code != 200: fails.append("history")

    # 15. Messages
    r = p("15. Messages", s.get(f"{BASE}/ta/{ta_id}/messages", timeout=15))
    if r.status_code != 200: fails.append("messages")

    # 16. CORS headers check
    print("\n=== CORS 检查 ===")
    headers = {
        "Origin": "https://cs-teachable-agent.xmeng19.workers.dev",
        "Access-Control-Request-Method": "GET",
    }
    r = s.options(f"{BASE}/health", headers=headers, timeout=15)
    cors_origin = r.headers.get("access-control-allow-origin", "MISSING")
    print(f"  CORS allow-origin for workers.dev: {cors_origin}")

    headers2 = {
        "Origin": "https://cs-teachable-agent.pages.dev",
        "Access-Control-Request-Method": "GET",
    }
    r2 = s.options(f"{BASE}/health", headers=headers2, timeout=15)
    cors_origin2 = r2.headers.get("access-control-allow-origin", "MISSING")
    print(f"  CORS allow-origin for pages.dev: {cors_origin2}")

    print(f"\n=== 结果 ===")
    if fails:
        print(f"  FAILED endpoints: {fails}")
        return 1
    print("  All 15 API endpoints passed!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
