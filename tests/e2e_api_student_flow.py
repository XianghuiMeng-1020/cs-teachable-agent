#!/usr/bin/env python3
"""
端到端 API 测试：模拟学生注册、登录、创建 TA、教学、测试、查看状态与历史。
运行方式（在项目根目录）: python tests/e2e_api_student_flow.py
"""
import os
import sys

# 确保可以导入 src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests

BASE = os.getenv("API_BASE", "http://127.0.0.1:8000/api")
USER = "e2e_student_test"
PASS = "testpass123"


def main():
    s = requests.Session()
    s.headers["Content-Type"] = "application/json"
    errors = []

    # 1. Health
    r = s.get(f"{BASE.replace('/api', '')}/api/health")
    assert r.status_code == 200, r.text
    print("1. GET /api/health OK")

    # 2. Config
    r = s.get(f"{BASE}/config")
    assert r.status_code == 200, r.text
    print("2. GET /api/config OK")

    # 3. Register
    r = s.post(f"{BASE}/auth/register", json={"username": USER, "password": PASS, "role": "student"})
    if r.status_code != 200:
        if "already registered" in r.text.lower():
            print("3. Register: user exists, will login")
        else:
            errors.append(f"Register: {r.status_code} {r.text}")
    else:
        print("3. POST /api/auth/register OK")

    # 4. Login
    r = s.post(f"{BASE}/auth/login", json={"username": USER, "password": PASS})
    if r.status_code != 200:
        errors.append(f"Login: {r.status_code} {r.text}")
        print("4. LOGIN FAILED")
        for e in errors:
            print("  ", e)
        return 1
    token = r.json()["access_token"]
    s.headers["Authorization"] = f"Bearer {token}"
    print("4. POST /api/auth/login OK")

    # 5. Me
    r = s.get(f"{BASE}/auth/me")
    assert r.status_code == 200, r.text
    print("5. GET /api/auth/me OK")

    # 6. List TA
    r = s.get(f"{BASE}/ta")
    assert r.status_code == 200, r.text
    tas = r.json()
    print("6. GET /api/ta OK, count:", len(tas))

    # 7. Create TA
    r = s.post(f"{BASE}/ta", json={"domain_id": "python", "name": "E2E Test TA"})
    if r.status_code != 200:
        errors.append(f"Create TA: {r.status_code} {r.text}")
    else:
        ta_id = r.json()["id"]
        print("7. POST /api/ta OK, ta_id:", ta_id)

        # 8. Teach
        r = s.post(f"{BASE}/ta/{ta_id}/teach", json={"student_input": "Variables store values. Use = to assign."})
        if r.status_code != 200:
            errors.append(f"Teach: {r.status_code} {r.text}")
        else:
            print("8. POST /api/ta/{id}/teach OK")

        # 9. State
        r = s.get(f"{BASE}/ta/{ta_id}/state")
        if r.status_code != 200:
            errors.append(f"State: {r.status_code} {r.text}")
        else:
            print("9. GET /api/ta/{id}/state OK")

        # 10. Problems
        r = s.get(f"{BASE}/ta/{ta_id}/problems")
        if r.status_code != 200:
            errors.append(f"Problems: {r.status_code} {r.text}")
        else:
            print("10. GET /api/ta/{id}/problems OK")

        # 11. Run test (optional problem_id)
        r = s.post(f"{BASE}/ta/{ta_id}/test", json={})
        if r.status_code != 200:
            errors.append(f"Test: {r.status_code} {r.text}")
        else:
            print("11. POST /api/ta/{id}/test OK")

        # 12. Mastery
        r = s.get(f"{BASE}/ta/{ta_id}/mastery")
        if r.status_code != 200:
            errors.append(f"Mastery: {r.status_code} {r.text}")
        else:
            print("12. GET /api/ta/{id}/mastery OK")

        # 13. History
        r = s.get(f"{BASE}/ta/{ta_id}/history?page=1&per_page=5")
        if r.status_code != 200:
            errors.append(f"History: {r.status_code} {r.text}")
        else:
            print("13. GET /api/ta/{id}/history OK")

        # 14. Messages
        r = s.get(f"{BASE}/ta/{ta_id}/messages")
        if r.status_code != 200:
            errors.append(f"Messages: {r.status_code} {r.text}")
        else:
            print("14. GET /api/ta/{id}/messages OK")

    if errors:
        print("\nErrors:")
        for e in errors:
            print(" ", e)
        return 1
    print("\nAll E2E API checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
