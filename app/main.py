from datetime import datetime
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.db_models import (
    InvestigationActionDB,
    InvestigationDB,
    InvestigationEventDB,
)
from app.investigation.evidence import collect_evidence
from app.models import Investigation, InvestigationAction, InvestigationCreate
from app.reasoning.classifier import classify_request
from app.reasoning.engine import diagnose


app = FastAPI(
    title="OpsPilot",
    description="AI-powered operations copilot",
    version="0.1.0",
)

Base.metadata.create_all(bind=engine)


def record_investigation_event(
    db: Session,
    investigation_id: str,
    event_type: str,
    from_status: str | None = None,
    to_status: str | None = None,
    message: str | None = None,
):
    event = InvestigationEventDB(
        id=str(uuid4()),
        investigation_id=investigation_id,
        event_type=event_type,
        from_status=from_status,
        to_status=to_status,
        message=message,
    )

    db.add(event)
    db.commit()


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

    record_investigation_event(
        db=db,
        investigation_id=investigation.id,
        event_type="investigation_created",
        from_status=None,
        to_status="analyzed",
        message="Investigation created and initial diagnosis completed",
    )

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

    if investigation.status != "analyzed":
        raise HTTPException(
            status_code=400,
            detail="Investigation must be analyzed before approval",
        )

    if not investigation.requires_human_approval:
        raise HTTPException(
            status_code=400,
            detail="Investigation does not require human approval",
        )

    old_status = investigation.status
    investigation.status = "approved"

    db.commit()
    db.refresh(investigation)

    record_investigation_event(
        db=db,
        investigation_id=investigation.id,
        event_type="investigation_approved",
        from_status=old_status,
        to_status=investigation.status,
        message="Investigation approved",
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


@app.post(
    "/api/v1/ops/investigations/{investigation_id}/complete",
    response_model=Investigation,
)
def complete_investigation(
    investigation_id: str,
    db: Session = Depends(get_db),
):
    investigation = db.get(InvestigationDB, investigation_id)

    if investigation is None:
        raise HTTPException(
            status_code=404,
            detail="Investigation not found",
        )

    if investigation.status != "approved":
        raise HTTPException(
            status_code=400,
            detail="Investigation must be approved before completion",
        )

    old_status = investigation.status
    investigation.status = "completed"

    db.commit()
    db.refresh(investigation)

    record_investigation_event(
        db=db,
        investigation_id=investigation.id,
        event_type="investigation_completed",
        from_status=old_status,
        to_status=investigation.status,
        message="Investigation completed",
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


@app.post(
    "/api/v1/ops/investigations/{investigation_id}/actions",
    response_model=InvestigationAction,
)
def create_action(
    investigation_id: str,
    db: Session = Depends(get_db),
):
    investigation = db.get(InvestigationDB, investigation_id)

    if investigation is None:
        raise HTTPException(
            status_code=404,
            detail="Investigation not found",
        )

    if investigation.status != "analyzed":
        raise HTTPException(
            status_code=400,
            detail="Investigation must be analyzed before creating an action",
        )

    if not investigation.recommended_action:
        raise HTTPException(
            status_code=400,
            detail="Investigation has no recommended action",
        )

    action = InvestigationActionDB(
        id=str(uuid4()),
        investigation_id=investigation.id,
        action_type="operational_remediation",
        description=investigation.recommended_action,
        status="proposed",
        requires_approval=True,
    )

    db.add(action)
    db.commit()
    db.refresh(action)

    record_investigation_event(
        db=db,
        investigation_id=investigation.id,
        event_type="action_created",
        from_status=None,
        to_status="proposed",
        message=f"Action created: {action.description}",
    )

    return InvestigationAction(
        id=action.id,
        investigation_id=action.investigation_id,
        action_type=action.action_type,
        description=action.description,
        status=action.status,
        requires_approval=action.requires_approval,
        result=action.result,
        created_at=(
            action.created_at.isoformat()
            if action.created_at
            else None
        ),
        executed_at=(
            action.executed_at.isoformat()
            if action.executed_at
            else None
        ),
    )

@app.post(
    "/api/v1/ops/investigations/{investigation_id}/actions/{action_id}/approve",
    response_model=InvestigationAction,
)
def approve_action(
    investigation_id: str,
    action_id: str,
    db: Session = Depends(get_db),
):
    investigation = db.get(InvestigationDB, investigation_id)
    if not investigation:
        raise HTTPException(status_code=404, detail="Investigation not found")

    action = db.get(InvestigationActionDB, action_id)
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")

    if action.investigation_id != investigation_id:
        raise HTTPException(
            status_code=400,
            detail="Action does not belong to investigation",
        )

    if action.status != "proposed":
        raise HTTPException(
            status_code=400,
            detail="Only proposed actions can be approved",
        )

    if not action.requires_approval:
        raise HTTPException(
            status_code=400,
            detail="Action does not require approval",
        )

    action.status = "approved"
    db.commit()
    db.refresh(action)

    record_investigation_event(
        db=db,
        investigation_id=investigation.id,
        event_type="action_approved",
        from_status="proposed",
        to_status="approved",
        message=f"Action approved: {action.description}",
    )

    return InvestigationAction(
        id=action.id,
        investigation_id=action.investigation_id,
        action_type=action.action_type,
        description=action.description,
        status=action.status,
        requires_approval=action.requires_approval,
        result=action.result,
        created_at=(
            action.created_at.isoformat()
            if action.created_at
            else None
        ),
        executed_at=(
            action.executed_at.isoformat()
            if action.executed_at
            else None
        ),
    )


@app.post(
    "/api/v1/ops/investigations/{investigation_id}/actions/{action_id}/execute",
    response_model=InvestigationAction,
)
def execute_action(
    investigation_id: str,
    action_id: str,
    db: Session = Depends(get_db),
):
    investigation = db.get(InvestigationDB, investigation_id)

    if investigation is None:
        raise HTTPException(
            status_code=404,
            detail="Investigation not found",
        )

    action = db.get(InvestigationActionDB, action_id)

    if action is None:
        raise HTTPException(
            status_code=404,
            detail="Action not found",
        )

    if action.investigation_id != investigation_id:
        raise HTTPException(
            status_code=400,
            detail="Action does not belong to this investigation",
        )

    if action.status != "approved":
        raise HTTPException(
            status_code=400,
            detail="Action must be approved before execution",
        )

    # Simulated execution.
    action.status = "executed"
    action.result = "Action executed successfully: operational remediation simulated"
    action.executed_at = datetime.utcnow()
    db.commit()
    db.refresh(action)

    record_investigation_event(
    db=db,
    investigation_id=investigation.id,
    event_type="action_executed",
    from_status="approved",
    to_status="executed",
    message=f"Action executed: {action.description}",
)
    return InvestigationAction(
        id=action.id,
        investigation_id=action.investigation_id,
        action_type=action.action_type,
        description=action.description,
        status=action.status,
        requires_approval=action.requires_approval,
        result=action.result,
        created_at=(
            action.created_at.isoformat()
            if action.created_at
            else None
        ),
        executed_at=(
            action.executed_at.isoformat()
            if action.executed_at
            else None
        ),
    )


@app.get(
    "/api/v1/ops/investigations/{investigation_id}/actions",
    response_model=list[InvestigationAction],
)
def list_actions(
    investigation_id: str,
    db: Session = Depends(get_db),
):
    investigation = db.get(InvestigationDB, investigation_id)

    if investigation is None:
        raise HTTPException(
            status_code=404,
            detail="Investigation not found",
        )

    actions = (
        db.query(InvestigationActionDB)
        .filter(
            InvestigationActionDB.investigation_id == investigation_id
        )
        .order_by(InvestigationActionDB.created_at.asc())
        .all()
    )

    return [
        InvestigationAction(
            id=action.id,
            investigation_id=action.investigation_id,
            action_type=action.action_type,
            description=action.description,
            status=action.status,
            requires_approval=action.requires_approval,
            result=action.result,
            created_at=(
                action.created_at.isoformat()
                if action.created_at
                else None
            ),
            executed_at=(
                action.executed_at.isoformat()
                if action.executed_at
                else None
            ),
        )
        for action in actions
    ]


@app.get(
    "/api/v1/ops/investigations/{investigation_id}/events",
)
def list_investigation_events(
    investigation_id: str,
    db: Session = Depends(get_db),
):
    investigation = db.get(InvestigationDB, investigation_id)

    if investigation is None:
        raise HTTPException(
            status_code=404,
            detail="Investigation not found",
        )

    events = (
        db.query(InvestigationEventDB)
        .filter(
            InvestigationEventDB.investigation_id == investigation_id
        )
        .order_by(InvestigationEventDB.created_at.asc())
        .all()
    )

    return [
        {
            "id": event.id,
            "investigation_id": event.investigation_id,
            "event_type": event.event_type,
            "from_status": event.from_status,
            "to_status": event.to_status,
            "message": event.message,
            "created_at": (
                event.created_at.isoformat()
                if event.created_at
                else None
            ),
        }
        for event in events
    ]
