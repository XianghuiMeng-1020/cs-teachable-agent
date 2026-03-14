"""
End-to-end test: register, login, create TA, teach, test.
Run with: pytest tests/test_e2e.py -v
Requires backend running at BASE_URL (default http://127.0.0.1:8000).
"""

import os
import pytest
import requests

BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:8000")


@pytest.fixture
def auth_headers():
    """Register a user, login, return Authorization header."""
    user = f"testuser_{os.urandom(4).hex()}"
    r = requests.post(f"{BASE_URL}/api/auth/register", json={
        "username": user,
        "password": "testpass",
        "role": "student",
    }, timeout=5)
    if r.status_code != 200:
        pytest.skip("Backend not available or register failed")
    r = requests.post(f"{BASE_URL}/api/auth/login", json={
        "username": user,
        "password": "testpass",
    }, timeout=5)
    assert r.status_code == 200
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_ta(auth_headers):
    r = requests.post(f"{BASE_URL}/api/ta", json={"domain_id": "python"}, headers=auth_headers, timeout=5)
    assert r.status_code == 200
    data = r.json()
    assert "id" in data
    assert data.get("domain_id") == "python"
    return data["id"]


def test_teach_and_test(auth_headers):
    ta_id = test_create_ta(auth_headers)
    r = requests.post(f"{BASE_URL}/api/ta/{ta_id}/teach", json={
        "student_input": "A variable stores a value. For example x = 5.",
    }, headers=auth_headers, timeout=10)
    assert r.status_code == 200
    body = r.json()
    assert "ta_response" in body
    assert "interpreted_units" in body

    r = requests.post(f"{BASE_URL}/api/ta/{ta_id}/test", json={}, headers=auth_headers, timeout=10)
    assert r.status_code == 200
    body = r.json()
    assert "passed" in body
    assert "ta_code" in body
    assert "mastery_report" in body
