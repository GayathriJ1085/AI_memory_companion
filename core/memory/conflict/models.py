from enum import Enum

from pydantic import BaseModel, Field

from core.memory.models import Memory


class ConflictDecision(str, Enum):
    CONFLICT = "CONFLICT"
    NO_CONFLICT = "NO_CONFLICT"
    REVIEW = "REVIEW"


class ConflictResult(BaseModel):
    decision: ConflictDecision

    reason: str = Field(min_length=1)

    existing_memory_id: str | None = None

    existing_memory: Memory | None = None