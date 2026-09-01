from enum import Enum

from pydantic import BaseModel, Field


class RelevanceDecision(str, Enum):
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"
    REVIEW = "REVIEW"


class RelevanceResult(BaseModel):
    decision: RelevanceDecision

    score: float = Field(ge=0.0, le=1.0)

    reason: str = Field(min_length=1)

    candidate_id: str | None = None