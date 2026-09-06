from enum import Enum

from pydantic import BaseModel, Field


class InvestigationStatus(str, Enum):
    CREATED = "created"
    INVESTIGATING = "investigating"
    ANALYZED = "analyzed"
    AWAITING_APPROVAL = "awaiting_approval"
    APPROVED = "approved"
    COMPLETED = "completed"
    FAILED = "failed"


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class InvestigationCreate(BaseModel):
    request: str = Field(
        min_length=1,
        description="The operational problem reported by the user.",
    )


class Investigation(BaseModel):
    id: str
    request: str
    status: InvestigationStatus = InvestigationStatus.CREATED
    severity: Severity | None = None
    diagnosis: str | None = None
    confidence: float | None = None
    evidence: list[str] | None = None
    recommended_action: str | None = None
    requires_human_approval: bool | None = None

class ActionStatus(str, Enum):
    PROPOSED = "proposed"
    APPROVED = "approved"
    EXECUTED = "executed"
    FAILED = "failed"


class InvestigationAction(BaseModel):
    id: str
    investigation_id: str
    action_type: str
    description: str
    status: ActionStatus = ActionStatus.PROPOSED
    requires_approval: bool = True
    result: str | None = None
    created_at: str | None = None
    executed_at: str | None = None