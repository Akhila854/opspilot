# OpsPilot

AI-powered operations copilot for evidence-based incident investigation, human-approved remediation, verification, and auditability.

OpsPilot turns an operational incident request into a structured investigation workflow:

```text
Incident Request
      ↓
Classification
      ↓
Operational Evidence
      ↓
AI Diagnosis
      ↓
Human Approval
      ↓
Remediation Proposal
      ↓
Human Approval
      ↓
Remediation Execution
      ↓
Verification
      ↓
Completed / Failed
      ↓
Persisted Audit Trail

The project is designed around an important operational principle:

AI can investigate and recommend actions, but remediation requires explicit human approval and every lifecycle transition is persisted for auditability.

Why OpsPilot?

Operational incidents often require engineers to combine several activities:

understand the incident request
classify the problem
collect relevant operational signals
determine a likely diagnosis
recommend a remediation
obtain approval before changing anything
execute the remediation
verify whether the system recovered
preserve an audit trail

OpsPilot demonstrates how these steps can be implemented as a backend workflow rather than treating an AI model as an unrestricted autonomous agent.

Key Features
Evidence-based investigation

An incoming incident request is classified and operational evidence is collected before diagnosis.

Example evidence:

API latency is 2400 ms
Error rate is 34.0%

The diagnosis is generated from the collected operational context.

AI diagnosis with deterministic fallback

OpsPilot integrates Gemini for incident reasoning.

If the external AI reasoning service is unavailable, the application falls back to deterministic reasoning logic.

This provides a predictable development and testing path without making the application completely dependent on an external AI service.

Conceptually:

Operational Evidence
        ↓
   Gemini Reasoning
        │
        ├── success → AI diagnosis
        │
        └── failure → deterministic fallback
Human approval gates

OpsPilot does not automatically execute remediation after diagnosis.

The investigation must first move through an approval step:

analyzed → approved

A remediation action also requires approval:

proposed → approved

This creates an explicit human-in-the-loop control point before operational actions are executed.

Remediation execution

Approved remediation actions can be executed through the API.

The current implementation simulates an operational remediation and produces post-remediation metrics such as:

{
  "error_rate": 1.5,
  "latency_ms": 180,
  "requests_per_minute": 1250,
  "database_connections": 100,
  "database_connection_limit": 100
}
Remediation verification

Execution is not considered successful simply because the action ran.

OpsPilot evaluates post-remediation metrics and records whether recovery was detected.

Example:

{
  "status": "completed",
  "recovered": true,
  "message": "Remediation verified successfully"
}
Persistent audit trail

Investigation and remediation lifecycle events are persisted.

For example:

investigation_created
        ↓
investigation_approved
        ↓
action_created
        ↓
action_approved
        ↓
action_executed
        ↓
action_verified

Each event records information such as:

event ID
investigation ID
event type
previous status
new status
event message
timestamp

This makes the complete operational workflow inspectable after execution.

Architecture
                    ┌─────────────────────┐
                    │     FastAPI API     │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       Investigations     Remediation        Audit
              │                │                │
              ▼                ▼                ▼
       Classification      Approval         Event Store
              │
              ▼
       Evidence Collection
              │
              ▼
       Reasoning Engine
          │         │
          │         └──────────────┐
          ▼                        ▼
       Gemini              Deterministic
       Reasoning              Fallback
          │                        │
          └──────────┬─────────────┘
                     ▼
              Persisted Diagnosis
                     │
                     ▼
               Human Approval
                     │
                     ▼
             Remediation Action
                     │
                     ▼
                  Execute
                     │
                     ▼
                 Verify
                     │
                     ▼
                Completed
Technology Stack
Area	Technology
API	FastAPI
Language	Python
Validation	Pydantic
ORM	SQLAlchemy
Database	SQLite
AI reasoning	Gemini
Server	Uvicorn
Testing	Pytest
Containerization	Docker
Local orchestration	Docker Compose
CI	GitHub Actions
API documentation	OpenAPI / Swagger UI
Frontend	HTML templates
Project Structure
opspilot/
│
├── app/
│   ├── database.py
│   ├── db_models.py
│   ├── main.py
│   ├── models.py
│   │
│   ├── investigation/
│   │   └── evidence.py
│   │
│   ├── reasoning/
│   │   ├── ai_engine.py
│   │   ├── classifier.py
│   │   ├── engine.py
│   │   └── schemas.py
│   │
│   ├── tools/
│   │   ├── logs.py
│   │   ├── metrics.py
│   │   ├── runbooks.py
│   │   └── services.py
│   │
│   └── templates/
│       ├── dashboard.html
│       └── investigation.html
│
├── tests/
│   ├── test_investigations.py
│   ├── test_openapi.py
│   └── test_reasoning.py
│
├── docs/
│   ├── architecture.md
│   └── api-workflow.md
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── .env.example
└── README.md
API Workflow
1. Create and analyze an investigation
POST /api/v1/ops/investigations

Example request:

{
  "request": "Payment API is returning 500 errors. Payment requests are intermittently failing with 500 errors and users are reporting timeouts."
}

The API:

creates the investigation
classifies the request
collects operational evidence
analyzes the evidence
persists the diagnosis
records an audit event
2. Approve the investigation
POST /api/v1/ops/investigations/{investigation_id}/approve

Moves:

analyzed → approved

This represents the human approval gate before remediation can be created.

3. Create a remediation action
POST /api/v1/ops/investigations/{investigation_id}/actions

Example action:

Investigate slow dependencies and review recent application changes

The action starts as:

proposed
4. Approve the remediation
POST /api/v1/ops/investigations/{investigation_id}/actions/{action_id}/approve

Moves:

proposed → approved
5. Execute the remediation
POST /api/v1/ops/investigations/{investigation_id}/actions/{action_id}/execute

The action moves to:

executed

Post-remediation operational metrics are produced.

6. Verify recovery
POST /api/v1/ops/investigations/{investigation_id}/actions/{action_id}/verify

If recovery conditions are satisfied:

executed → completed

Otherwise the workflow can record a failed verification state.

7. Inspect the audit trail
GET /api/v1/ops/investigations/{investigation_id}/events

This returns the persisted lifecycle events for the investigation.

Example End-to-End Investigation

A portfolio demonstration uses a simulated Payment API incident.

Incident
Payment API is returning 500 errors.
Payment requests are intermittently failing with 500 errors
and users are reporting timeouts.
Diagnosis
Severity: high
Diagnosis: High API latency
Confidence: 0.88
Evidence
API latency is 2400 ms
Error rate is 34.0%
Recommended remediation
Investigate slow dependencies and review recent application changes
Post-remediation metrics
Error rate: 1.5%
Latency: 180 ms
Requests/minute: 1250
Database connections: 100
Database connection limit: 100
Verification
Status: completed
Recovered: true
Audit lifecycle
investigation_created
investigation_approved
action_created
action_approved
action_executed
action_verified

This demonstrates the complete workflow from incident intake through verified recovery.

Running Locally
1. Clone the repository
git clone https://github.com/Akhila854/opspilot.git
cd opspilot
2. Create a virtual environment

Windows PowerShell:

python -m venv .venv
.\.venv\Scripts\Activate.ps1
3. Install dependencies
python -m pip install -r requirements-dev.txt
4. Configure environment variables

Copy:

.env.example

to:

.env

Configure the Gemini credentials if AI reasoning is required.

Do not commit .env or API keys to Git.

5. Start the API
python -m uvicorn app.main:app --reload

The application will be available at:

http://127.0.0.1:8000

Swagger documentation:

http://127.0.0.1:8000/docs
Running Tests

Run the complete test suite:

pytest -q

The project currently has automated coverage for:

investigation creation
investigation state transitions
pagination validation
remediation action workflow
audit events
reasoning behavior
API/OpenAPI structure

Latest local verification:

17 passed

Additional checks:

python -m compileall app
git diff --check
git status --short
Docker

Build and start OpsPilot with Docker Compose:

docker compose up --build

The API will be available at:

http://127.0.0.1:8000

Stop the application:

docker compose down

The SQLite database is persisted through the Docker Compose volume.

CI

GitHub Actions runs automated validation on the repository.

The CI workflow performs checks including:

Install dependencies
        ↓
Compile application
        ↓
Run pytest
        ↓
Check git diff

This ensures that changes pushed to the repository are automatically validated.

API Documentation

OpsPilot exposes an OpenAPI 3.1 specification through FastAPI.

Swagger UI:

/docs

OpenAPI specification:

/openapi.json

The API is organized into:

System
Investigations
Remediation
Audit
Design Principles
Human-in-the-loop

AI recommendations do not directly authorize operational changes.

Approval is explicitly represented in the workflow.

Evidence before diagnosis

The reasoning process receives operational evidence rather than relying only on the original incident text.

Deterministic fallback

The application remains usable when external AI reasoning is unavailable.

Verification after execution

Executing an action is separate from determining whether the system recovered.

Persistent auditability

Important state transitions are recorded as durable events.

Explicit state transitions

Investigation and remediation states are validated rather than allowing arbitrary transitions.

What This Project Demonstrates

OpsPilot was built to demonstrate practical backend and AI engineering concepts:

FastAPI API design
RESTful workflow modeling
Pydantic validation
SQLAlchemy persistence
SQLite database design
AI integration with Gemini
deterministic fallback reasoning
operational evidence collection
state machines and guarded transitions
human approval workflows
remediation execution
post-action verification
audit logging
API pagination and filtering
automated testing
OpenAPI documentation
Docker containerization
Docker Compose
GitHub Actions CI
structured project documentation
Project Status

The core OpsPilot workflow is implemented and tested.

The current implementation provides an end-to-end demonstration of:

Investigation
→ Diagnosis
→ Approval
→ Remediation
→ Approval
→ Execution
→ Verification
→ Audit

The remediation layer currently uses simulated operational actions, making the project safe to demonstrate locally while preserving the architecture needed for future integrations with real operational systems.

Future Extensions

Possible future integrations include:

real log platforms
Prometheus metrics
Kubernetes health checks
cloud monitoring APIs
incident-management systems
Slack or Microsoft Teams notifications
production runbook execution
role-based approval permissions
richer remediation policies

These are intentionally outside the current core implementation.

Author

Akhila

Backend / AI Engineering Portfolio Project

GitHub:

https://github.com/Akhila854/opspilot