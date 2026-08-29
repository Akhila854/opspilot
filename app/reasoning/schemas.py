from pydantic import BaseModel, Field


class Diagnosis(BaseModel):
    diagnosis: str = Field(
        min_length=1,
        description="The most likely root cause of the incident.",
    )

    severity: str = Field(
        min_length=1,
        description="The assessed severity of the incident.",
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence in the diagnosis, between 0 and 1.",
    )

    evidence: list[str] = Field(
        min_length=1,
        description="Evidence supporting the diagnosis.",
    )

    recommended_action: str = Field(
        min_length=1,
        description="Recommended next operational action.",
    )

    requires_human_approval: bool = Field(
        description="Whether human approval is required before taking action.",
    )