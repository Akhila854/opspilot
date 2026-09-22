# OpsPilot API Workflow

OpsPilot exposes an HTTP API for an evidence-based incident investigation workflow.

The interactive API documentation is available at:

`http://127.0.0.1:8000/docs`

## Workflow

```text
Create investigation
        |
        v
Classify request
        |
        v
Collect operational evidence
        |
        v
AI diagnosis
        |
        +---- Gemini unavailable
        |          |
        |          v
        |    Deterministic fallback
        |
        v
Investigation: analyzed
        |
        v
Human approval
        |
        v
Investigation: approved
        |
        v
Create remediation action
        |
        v
Action: proposed
        |
        v
Human approval
        |
        v
Action: approved
        |
        v
Execute remediation
        |
        v
Action: executed
        |
        v
Verify operational metrics
        |
        +---- Recovery successful ---> Investigation: completed
        |
        +---- Recovery unsuccessful -> Investigation: failed
Core endpoints
Investigation lifecycle
Method    Endpoint    Purpose
POST    /api/v1/ops/investigations    Create and analyze an investigation
GET    /api/v1/ops/investigations    List investigations
GET    /api/v1/ops/investigations/{investigation_id}    Retrieve an investigation
POST    /api/v1/ops/investigations/{investigation_id}/approve    Approve an investigation
POST    /api/v1/ops/investigations/{investigation_id}/complete    Complete an approved investigation
Remediation lifecycle
Method    Endpoint    Purpose
POST    /api/v1/ops/investigations/{investigation_id}/actions    Create the recommended action
GET    /api/v1/ops/investigations/{investigation_id}/actions    List actions
POST    /api/v1/ops/investigations/{investigation_id}/actions/{action_id}/approve    Approve an action
POST    /api/v1/ops/investigations/{investigation_id}/actions/{action_id}/execute    Execute an approved action
POST    /api/v1/ops/investigations/{investigation_id}/actions/{action_id}/verify    Verify remediation
Audit
Method    Endpoint    Purpose
GET    /api/v1/ops/investigations/{investigation_id}/events    Retrieve persisted lifecycle events
Safety model

The API intentionally separates recommendation from execution.

Diagnosis produces a recommended action.
A human must approve the investigation.
The remediation action is created separately.
The remediation action requires another approval.
Only an approved action can execute.
Verification checks operational metrics after execution.
Lifecycle events are persisted for auditability.
Example demo sequence

Use Swagger UI to execute the workflow interactively:

POST /api/v1/ops/investigations
POST /api/v1/ops/investigations/{id}/approve
POST /api/v1/ops/investigations/{id}/actions
POST /api/v1/ops/investigations/{id}/actions/{action_id}/approve
POST /api/v1/ops/investigations/{id}/actions/{action_id}/execute
POST /api/v1/ops/investigations/{id}/actions/{action_id}/verify
GET /api/v1/ops/investigations/{id}/events

The remediation implementation is simulated, so this workflow demonstrates controlled operations without modifying real infrastructure.
