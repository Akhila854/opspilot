from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException
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

    # Step 5: Persist the full diagnosis.
    investigation.status = "analyzed"
    investigation.severity = diagnosis.severity
    investigation.diagnosis = diagnosis.diagnosis
    investigation.confidence = diagnosis.confidence
    investigation.evidence = diagnosis.evidence
    investigation.recommended_action = diagnosis.recommended_action
    investigation.requires_human_approval = diagnosis.requires_human_approval

    db.commit()
    db.refresh(investigation)

    # Step 6: Return the complete investigation.
    return Investigation(
        id=investigation.id,
        request=investigation.request,
        status=investigation.status,
        severity=investigation.severity,
        diagnosis=investigation.diagnosis,
        confidence=investigation.confidence,
        evidence=investigation.evidence,
        recommended_action=investigation.recommended_action,
        requires_human_approval=investigation.requires_human_approval,
    )



@app.get(
    "/api/v1/ops/investigations/{investigation_id}",
    response_model=Investigation,
)
def get_investigation(
    investigation_id: str,
    db: Session = Depends(get_db),
):
    investigation = db.get(InvestigationDB, investigation_id)

    if investigation is None:

        raise HTTPException(
            status_code=404,
            detail="Investigation not found",
        )

    return Investigation(
        id=investigation.id,
        request=investigation.request,
        status=investigation.status,
        severity=investigation.severity,
        diagnosis=investigation.diagnosis,
        confidence=investigation.confidence,
        evidence=investigation.evidence,
        recommended_action=investigation.recommended_action,
        requires_human_approval=investigation.requires_human_approval,
    )

@app.get(
    "/api/v1/ops/investigations",
    response_model=list[Investigation],
)
def list_investigations(
    db: Session = Depends(get_db),
):
    investigations = (
        db.query(InvestigationDB)
        .order_by(InvestigationDB.id.desc())
        .all()
    )

    return [
        Investigation(
            id=investigation.id,
            request=investigation.request,
            status=investigation.status,
            severity=investigation.severity,
            diagnosis=investigation.diagnosis,
            confidence=investigation.confidence,
            evidence=investigation.evidence,
            recommended_action=investigation.recommended_action,
            requires_human_approval=investigation.requires_human_approval,
        )
        for investigation in investigations
    ]

@app.post(
    "/api/v1/ops/investigations/{investigation_id}/approve",
    response_model=Investigation,
)
def approve_investigation(
    investigation_id: str,
    db: Session = Depends(get_db),
):
    investigation = db.get(InvestigationDB, investigation_id)

    if investigation is None:
        raise HTTPException(
            status_code=404,
            detail="Investigation not found",
        )

    if not investigation.requires_human_approval:
        raise HTTPException(
            status_code=400,
            detail="Investigation does not require human approval",
        )

    investigation.status = "approved"

    db.commit()
    db.refresh(investigation)

    return Investigation(
        id=investigation.id,
        request=investigation.request,
        status=investigation.status,
        severity=investigation.severity,
        diagnosis=investigation.diagnosis,
        confidence=investigation.confidence,
        evidence=investigation.evidence,
        recommended_action=investigation.recommended_action,
        requires_human_approval=investigation.requires_human_approval,
    )