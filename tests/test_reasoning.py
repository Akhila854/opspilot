from app.reasoning.classifier import classify_request
from app.investigation.evidence import collect_evidence
from app.reasoning.engine import diagnose
from app.reasoning.ai_engine import build_diagnosis_prompt
from app.tools.metrics import reset_metrics


def setup_function():
    reset_metrics()


def test_high_api_latency_diagnosis():
    classification = classify_request("Payment API is experiencing high latency and timeouts")
    evidence = collect_evidence(**classification)
    diagnosis = diagnose(evidence)

    assert classification["incident_type"] == "high_api_latency"
    assert diagnosis.diagnosis == "High API latency"
    assert diagnosis.severity == "high"
    assert diagnosis.confidence == 0.88
    assert diagnosis.requires_human_approval is True


def test_authentication_failure_diagnosis():
    classification = classify_request("Users are experiencing authentication failures and login errors")
    evidence = collect_evidence(**classification)
    diagnosis = diagnose(evidence)

    assert classification["incident_type"] == "authentication_failure"
    assert diagnosis.diagnosis == "Authentication service failure"
    assert diagnosis.severity == "high"
    assert diagnosis.confidence == 0.86
    assert diagnosis.requires_human_approval is True

def test_ai_diagnosis_prompt_contains_operational_evidence():
    evidence = {
        "service": "payment-api",
        "incident_type": "database_connection_exhaustion",
        "logs": ["Database connection timeout", "Connection pool exhausted"],
        "metrics": {
            "error_rate": 34.0,
            "latency_ms": 2400,
            "db_connections": "100/100",
        },
    }

    prompt = build_diagnosis_prompt(evidence)

    assert "payment-api" in prompt
    assert "database_connection_exhaustion" in prompt
    assert "Connection pool exhausted" in prompt
    assert "Analyze ONLY the supplied operational evidence" in prompt
    assert "Do not invent facts or evidence" in prompt
