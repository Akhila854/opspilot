from uuid import uuid4

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.database import get_db
from app.db_models import InvestigationDB
from app.investigation.evidence import collect_evidence
from app.models import Investigation, InvestigationCreate
from app.reasoning.classifier import classify_request
from app.reasoning.engine import diagnose


app = FastAPI(
    title="OpsPilot",
    description="AI-powered operations copilot",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post(
    "/api/v1/ops/investigations",
    response_model=Investigation,
)
def create_investigation(
    payload: InvestigationCreate,
    db: Session = Depends(get_db),
):
    # Step 1: Create the investigation record.
    investigation = InvestigationDB(
        id=str(uuid4()),
        request=payload.request,
    )

    db.add(investigation)
    db.commit()
    db.refresh(investigation)

    # Step 2: Classify the investigation request.
    classification = classify_request(payload.request)

    # Step 3: Collect operational evidence.
    evidence = collect_evidence(**classification)

    # Step 4: Analyze the evidence.
    diagnosis = diagnose(evidence)

    # Step 5: Update the investigation with the diagnosis.
    investigation.status = "analyzed"
    investigation.severity = diagnosis.severity

    db.commit()
    db.refresh(investigation)

    # Step 6: Return the investigation.
    return Investigation(
        id=investigation.id,
        request=investigation.request,
        status=investigation.status,
        severity=investigation.severity,
    )