# OpsPilot

**AI-powered operations copilot for incident investigation, diagnosis, human-approved remediation, verification, and auditability.**

OpsPilot is a FastAPI backend that turns an operational incident request into a structured, evidence-based investigation and controlled remediation workflow.

The project demonstrates how AI can assist with operational diagnosis while keeping **human approval, execution controls, persistence, and auditability** in the loop.

---

## What OpsPilot Does

Given an incident such as:

```text
Payment API is timing out because the database connection pool is exhausted
```

OpsPilot:

1. Classifies the incident
2. Collects operational evidence
3. Analyzes the evidence
4. Produces a diagnosis, severity, and confidence score
5. Recommends a remediation
6. Requires human approval
7. Creates a controlled remediation action
8. Requires approval for the action
9. Executes the remediation
10. Verifies whether the system recovered
11. Marks the investigation completed or failed
12. Records the lifecycle in an audit trail

The core principle is:

> **AI can recommend operational actions, but execution remains controlled, verifiable, and auditable.**

---

## Architecture

```text
                         ┌──────────────────┐
                         │      Client      │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │     FastAPI      │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │   Classification │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Evidence         │
                         │ Collection       │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ AI / Deterministic│
                         │ Diagnosis Engine  │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Recommended      │
                         │ Remediation      │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Human Approval   │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Action Approval  │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Remediation      │
                         │ Execution        │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Recovery         │
                         │ Verification     │
                         └────────┬─────────┘
                                  │
                         ┌────────┴────────┐
                         ▼                 ▼
                    ┌──────────┐      ┌──────────┐
                    │Completed │      │  Failed  │
                    └──────────┘      └──────────┘
                         │                 │
                         └────────┬────────┘
                                  ▼
                         ┌──────────────────┐
                         │ Audit Trail      │
                         │ + SQLite         │
                         └──────────────────┘
```

---

## Investigation Lifecycle

```text
created
   │
   ▼
analyzed
   │
   ▼
human approval
   │
   ▼
approved
   │
   ▼
action proposed
   │
   ▼
action approved
   │
   ▼
action executed
   │
   ▼
verification
   │
   ├──────────────► completed
   │
   └──────────────► failed
```

This separates **diagnosis**, **authorization**, **execution**, and **verification** rather than treating an AI recommendation as an automatic operational change.

---

## Example Investigation

### Request

```text
Payment API is timing out because the database connection pool is exhausted
```

### Diagnosis

```text
Severity: critical
Diagnosis: Database connection pool exhaustion
Confidence: 0.94
Human approval required: true
```

### Evidence

```text
Database connections: 100/100
Database timeout logs: detected
Error rate: 34.0%
Latency: 2400 ms
```

### Recommended Remediation

```text
Investigate connection leaks and verify PostgreSQL health
```

### Post-Remediation Verification

After the simulated remediation:

```text
Database connections: 42/100
Error rate: 2.0%
Latency: 180 ms
Recovered: true
Status: completed
```

This means the system does not stop at:

> "I think I fixed it."

It verifies the operational state after execution.

---

## AI Reasoning

OpsPilot supports Gemini-based incident reasoning while retaining a deterministic diagnosis path as a fallback.

The reasoning pipeline is designed around supplied operational evidence rather than allowing the model to invent infrastructure facts.

The AI diagnosis produces structured information including:

* Diagnosis
* Severity
* Confidence
* Evidence
* Recommended action
* Human approval requirement

If AI reasoning is unavailable, OpsPilot can fall back to deterministic diagnosis logic.

---

## Controlled Remediation

Remediation actions follow their own approval lifecycle:

```text
proposed
   │
   ▼
approved
   │
   ▼
executed
```

Execution is currently simulated so the project can demonstrate the complete operational workflow without making destructive changes to real infrastructure.

After execution, OpsPilot evaluates simulated operational metrics to determine whether the incident recovered.

---

## Auditability

OpsPilot records lifecycle events such as:

```text
investigation_created
investigation_approved
action_created
action_approved
action_executed
action_verified
```

This provides an audit trail showing how an incident moved through diagnosis, approval, remediation, and verification.

---

## API

| Method | Endpoint                                                      | Purpose                   |
| ------ | ------------------------------------------------------------- | ------------------------- |
| GET    | `/health`                                                     | Health check              |
| POST   | `/api/v1/ops/investigations`                                  | Create investigation      |
| GET    | `/api/v1/ops/investigations`                                  | List investigations       |
| GET    | `/api/v1/ops/investigations/{id}`                             | Get investigation         |
| POST   | `/api/v1/ops/investigations/{id}/approve`                     | Approve investigation     |
| POST   | `/api/v1/ops/investigations/{id}/actions`                     | Create remediation action |
| POST   | `/api/v1/ops/investigations/{id}/actions/{action_id}/approve` | Approve action            |
| POST   | `/api/v1/ops/investigations/{id}/actions/{action_id}/execute` | Execute action            |
| POST   | `/api/v1/ops/investigations/{id}/actions/{action_id}/verify`  | Verify remediation        |
| GET    | `/api/v1/ops/investigations/{id}/actions`                     | List actions              |
| GET    | `/api/v1/ops/investigations/{id}/events`                      | View audit trail          |
| POST   | `/api/v1/ops/investigations/{id}/complete`                    | Complete investigation    |

Interactive API documentation is available through FastAPI:

```text
http://127.0.0.1:8000/docs
```

---

## Tech Stack

* Python 3.12
* FastAPI
* Pydantic
* SQLAlchemy
* SQLite
* Google Gemini
* Pytest
* Docker
* Docker Compose
* PowerShell

---

## Persistence

OpsPilot uses SQLite through SQLAlchemy.

Docker mounts the database into a named volume:

```text
SQLite
  │
  ▼
/app/data/opspilot.db
  │
  ▼
Docker named volume
```

This allows investigation data to survive container recreation.

The persistence workflow has been verified by creating an investigation, recreating the Docker container, and retrieving the same investigation afterward.

---

## Running Locally

Create and activate the virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Start the API:

```powershell
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

## Running with Docker

Build and start:

```powershell
docker compose up --build
```

Check the service:

```powershell
docker compose ps
```

Health check:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

Expected:

```text
status
------
healthy
```

---

## Testing

Run the complete test suite:

```powershell
pytest -q
```

The project includes automated coverage for:

* Health checks
* Investigation creation
* Classification
* Evidence collection
* Deterministic diagnosis
* AI diagnosis prompt construction
* Investigation approval
* Remediation actions
* Action approval
* Action execution
* Audit trails
* Pagination validation
* Evidence collection failures

---

## Project Structure

```text
opspilot/
│
├── app/
│   ├── main.py
│   ├── models.py
│   ├── db_models.py
│   ├── database.py
│   │
│   ├── investigation/
│   │   └── evidence.py
│   │
│   ├── reasoning/
│   │   ├── classifier.py
│   │   ├── engine.py
│   │   ├── ai_engine.py
│   │   └── schemas.py
│   │
│   └── tools/
│       ├── logs.py
│       ├── metrics.py
│       ├── services.py
│       └── runbooks.py
│
├── tests/
│   ├── test_investigations.py
│   └── test_reasoning.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
├── .env.example
└── README.md
```

---

## Design Principles

### Human-in-the-loop

AI recommendations do not directly trigger operational remediation.

### Evidence-based reasoning

Diagnosis is based on collected operational evidence rather than unrestricted model speculation.

### Controlled execution

Remediation requires explicit approval before execution.

### Verification

A remediation is not considered successful merely because execution completed. Operational metrics are checked afterward.

### Auditability

Investigation and action lifecycle events are persisted for traceability.

### Safe simulation

The remediation layer is simulated, making the project suitable for development and demonstration without modifying real production infrastructure.

---

## Future Improvements

Potential next steps include:

* PostgreSQL production support
* Real observability integrations
* Kubernetes and cloud integrations
* Authentication and authorization
* Role-based approval policies
* Real remediation adapters
* Background investigation jobs
* Distributed tracing
* Metrics and monitoring dashboards
* Production-grade database migrations

---

## Why OpsPilot?

OpsPilot demonstrates a practical approach to AI-assisted operations:

**investigate → reason → approve → remediate → verify → audit**

The project focuses not just on generating an AI answer, but on integrating AI into a controlled operational workflow where actions require authorization and outcomes are verified.

> **Automation should increase operational speed without removing human control.**
