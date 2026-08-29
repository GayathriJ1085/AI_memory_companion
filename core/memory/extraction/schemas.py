from enum import Enum

from pydantic import BaseModel, Field


class MemoryType(str, Enum):
    PERSONAL_FACT = "PERSONAL_FACT"
    RELATIONSHIP = "RELATIONSHIP"
    PREFERENCE = "PREFERENCE"
    PLACE = "PLACE"
    EVENT = "EVENT"
    ROUTINE = "ROUTINE"
    TEMPORARY_CONTEXT = "TEMPORARY_CONTEXT"


class EvidenceType(str, Enum):
    EXPLICIT_USER_STATEMENT = "EXPLICIT_USER_STATEMENT"
    USER_CORRECTION = "USER_CORRECTION"
    REPEATED_OBSERVATION = "REPEATED_OBSERVATION"
    SYSTEM_INFERENCE = "SYSTEM_INFERENCE"
    USER_PROVIDED_DATA = "USER_PROVIDED_DATA"


class MemoryCandidate(BaseModel):
    type: MemoryType

    subject: str = Field(min_length=1)

    predicate: str = Field(min_length=1)

    value: str = Field(min_length=1)

    content: str = Field(min_length=1)

    evidence_type: EvidenceType

    source_text: str = Field(min_length=1)


class ExtractionResult(BaseModel):
    candidates: list[MemoryCandidate]