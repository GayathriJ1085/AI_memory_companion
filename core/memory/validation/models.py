from enum import Enum

from pydantic import BaseModel, Field


class ValidationDecision(str, Enum):
    VALID = "VALID"
    INVALID = "INVALID"
    REVIEW = "REVIEW"


class ValidationResult(BaseModel):
    decision: ValidationDecision

    reason: str = Field(min_length=1)

    candidate_id: str | None = None