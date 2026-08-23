from uuid import uuid4

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.database import get_db
from app.db_models import InvestigationDB
from app.models import Investigation, InvestigationCreate


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
    investigation = InvestigationDB(
        id=str(uuid4()),
        request=payload.request,
    )

    db.add(investigation)
    db.commit()
    db.refresh(investigation)

    return Investigation(
        id=investigation.id,
        request=investigation.request,
        status=investigation.status,
        severity=investigation.severity,
    )