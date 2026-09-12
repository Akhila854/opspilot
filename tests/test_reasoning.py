from app.reasoning.classifier import classify_request
from app.investigation.evidence import collect_evidence
from app.reasoning.engine import diagnose


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
