from app.main import app


def test_openapi_documents_ops_workflow():
    schema = app.openapi()

    assert schema["info"]["title"] == "OpsPilot"
    assert len(schema["tags"]) == 4

    create_operation = schema["paths"]["/api/v1/ops/investigations"]["post"]
    assert create_operation["tags"] == ["Investigations"]
    assert create_operation["summary"] == "Create and analyze an investigation"

    approve_operation = schema["paths"][
        "/api/v1/ops/investigations/{investigation_id}/approve"
    ]["post"]
    assert approve_operation["tags"] == ["Investigations"]

    execute_operation = schema["paths"][
        "/api/v1/ops/investigations/{investigation_id}/actions/{action_id}/execute"
    ]["post"]
    assert execute_operation["tags"] == ["Remediation"]

    verify_operation = schema["paths"][
        "/api/v1/ops/investigations/{investigation_id}/actions/{action_id}/verify"
    ]["post"]
    assert verify_operation["tags"] == ["Remediation"]

    events_operation = schema["paths"][
        "/api/v1/ops/investigations/{investigation_id}/events"
    ]["get"]
    assert events_operation["tags"] == ["Audit"]
