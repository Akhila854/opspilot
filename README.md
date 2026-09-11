# OpsPilot

AI-powered operations copilot for incident investigation, diagnosis, human-approved remediation, and auditability.

## Overview

OpsPilot is a FastAPI backend that turns an operational incident request into a structured investigation.

The system:

1. Receives an incident request
2. Classifies the request and determines severity
3. Collects operational evidence
4. Produces a diagnosis with confidence
5. Recommends a remediation action
6. Requires human approval before remediation
7. Tracks action execution
8. Maintains an audit trail

> AI can recommend operational actions, but execution should remain controlled and auditable.

## Architecture

```text
Client -> FastAPI -> Classification -> Evidence -> Diagnosis
                                      |
                                      v
                              Recommended Action
                                      |
                                      v
                               Human Approval
                                      |
                                      v
                              Action Execution
                                      |
                                      v
                                Audit Trail
                                      |
                                      v
                            SQLAlchemy + SQLite
```

## Example

Request:

```text
Database connection pool is exhausted and requests are timing out
```

Result:

- Severity: critical
- Diagnosis: Database connection pool exhaustion
- Confidence: 0.94
- Evidence: database connections at 100/100, timeout logs, elevated error rate, high latency
- Recommended action: Investigate connection leaks and verify PostgreSQL health
- Human approval required: true

## Remediation Workflow

```text
proposed -> approved -> executed
```

Remediation execution is currently simulated so the workflow can be demonstrated safely.

## Audit Trail

OpsPilot records investigation and action lifecycle events including creation, approval, and execution.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/api/v1/ops/investigations` | Create investigation |
| GET | `/api/v1/ops/investigations` | List investigations |
| GET | `/api/v1/ops/investigations/{id}` | Get investigation |
| POST | `/api/v1/ops/investigations/{id}/actions` | Create remediation action |
| POST | `/api/v1/ops/investigations/{id}/actions/{action_id}/approve` | Approve action |
| POST | `/api/v1/ops/investigations/{id}/actions/{action_id}/execute` | Execute action |
| GET | `/api/v1/ops/investigations/{id}/actions` | List actions |
| GET | `/api/v1/ops/investigations/{id}/events` | View audit trail |

## Tech Stack

- Python 3.12
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite
- Pytest
- Docker
- Docker Compose

## Run Locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API documentation: `http://127.0.0.1:8000/docs`

## Docker

```powershell
docker compose up --build
```

## Testing

```powershell
pytest -q
```

The test suite covers health checks, investigation creation, diagnosis, remediation approval, execution, and audit trails.

## Project Structure

```text
opspilot/
  app/
    main.py
    models.py
    database.py
    db_models.py
  tests/
    test_investigations.py
  Dockerfile
  docker-compose.yml
  requirements.txt
  pytest.ini
  .env.example
  README.md
```

## Future Improvements

- Real LLM-based investigation reasoning
- PostgreSQL production support
- Observability integrations
- Kubernetes/cloud integrations
- Authentication and authorization
- Role-based approval policies
- Production remediation adapters

## Why OpsPilot?

OpsPilot demonstrates incident investigation, operational evidence, diagnosis, confidence-based reasoning, human-in-the-loop approval, controlled remediation, persistence, auditability, automated testing, and containerized deployment.

> Automation should increase operational speed without removing human control.
