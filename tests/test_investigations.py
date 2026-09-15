from unittest.mock import patch

from app.reasoning.schemas import Diagnosis

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

def mock_gemini_diagnosis():
    return Diagnosis(
        diagnosis="Database connection pool exhaustion",
        severity="critical",
        confidence=0.94,
        evidence=["Database connections are at 100/100"],
        recommended_action="Investigate connection leaks and verify PostgreSQL health",
        requires_human_approval=True,
    )


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@patch("app.main.diagnose_with_ai", side_effect=mock_gemini_diagnosis)
def test_create_investigation(mock_gemini):
    response = client.post(
        "/api/v1/ops/investigations",
        json={
            "request": "Database connection pool is exhausted and requests are timing out"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "analyzed"
    assert data["severity"] == "critical"
    assert data["diagnosis"] == "Database connection pool exhaustion"
    assert data["confidence"] == 0.94
    assert data["requires_human_approval"] is True
    assert len(data["evidence"]) > 0


@patch("app.main.diagnose_with_ai", side_effect=mock_gemini_diagnosis)
def test_investigation_action_workflow(mock_gemini):
    response = client.post(
        "/api/v1/ops/investigations",
        json={
            "request": "Database connection pool is exhausted and requests are timing out"
        },
    )

    assert response.status_code == 200

    investigation = response.json()
    investigation_id = investigation["id"]

    action_response = client.post(
        f"/api/v1/ops/investigations/{investigation_id}/actions"
    )

    assert action_response.status_code == 200

    action = action_response.json()
    action_id = action["id"]

    assert action["status"] == "proposed"
    assert action["requires_approval"] is True

    approve_response = client.post(
        f"/api/v1/ops/investigations/{investigation_id}/actions/{action_id}/approve"
    )

    assert approve_response.status_code == 200
    assert approve_response.json()["status"] == "approved"

    execute_response = client.post(
        f"/api/v1/ops/investigations/{investigation_id}/actions/{action_id}/execute"
    )

    assert execute_response.status_code == 200

    executed_action = execute_response.json()

    assert executed_action["status"] == "executed"
    assert executed_action["result"] is not None
    assert executed_action["executed_at"] is not None


@patch("app.main.diagnose_with_ai", side_effect=mock_gemini_diagnosis)
def test_action_audit_trail(mock_gemini):
    response = client.post(
        "/api/v1/ops/investigations",
        json={
            "request": "Database connection pool is exhausted and requests are timing out"
        },
    )

    investigation_id = response.json()["id"]

    action_response = client.post(
        f"/api/v1/ops/investigations/{investigation_id}/actions"
    )

    action_id = action_response.json()["id"]

    client.post(
        f"/api/v1/ops/investigations/{investigation_id}/actions/{action_id}/approve"
    )

    client.post(
        f"/api/v1/ops/investigations/{investigation_id}/actions/{action_id}/execute"
    )

    events_response = client.get(
        f"/api/v1/ops/investigations/{investigation_id}/events"
    )

    assert events_response.status_code == 200

    event_types = [
        event["event_type"]
        for event in events_response.json()
    ]

    assert event_types == [
        "investigation_created",
        "action_created",
        "action_approved",
        "action_executed",
    ]

def test_list_investigations_filters():
    client.post(
        "/api/v1/ops/investigations",
        json={
            "request": "Database connection pool is exhausted and requests are timing out"
        },
    )

    response = client.get(
        "/api/v1/ops/investigations?severity=critical"
    )

    assert response.status_code == 200

    investigations = response.json()

    assert len(investigations) > 0
    assert all(
        investigation["severity"] == "critical"
        for investigation in investigations
    )

def test_list_investigations_pagination():
    client.post(
        "/api/v1/ops/investigations",
        json={
            "request": "Database connection pool is exhausted and requests are timing out"
        },
    )

    first_page = client.get(
        "/api/v1/ops/investigations?limit=1&offset=0"
    )

    second_page = client.get(
        "/api/v1/ops/investigations?limit=1&offset=1"
    )

    assert first_page.status_code == 200
    assert second_page.status_code == 200

    first_results = first_page.json()
    second_results = second_page.json()

    assert len(first_results) == 1
    assert len(second_results) == 1

    assert first_results[0]["id"] != second_results[0]["id"]