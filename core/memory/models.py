from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field


class MemoryStatus(str, Enum):
    ACTIVE = "ACTIVE"
    SUPERSEDED = "SUPERSEDED"
    REJECTED = "REJECTED"


class Memory(BaseModel):
    """
    A trusted personal memory maintained by the memory system.

    A Memory is different from a MemoryCandidate.

    MemoryCandidate:
        Information extracted from a conversation that still needs
        processing.

    Memory:
        Information that has passed the required memory-processing
        stages and can be stored/retrieved.
    """

    id: str = Field(default_factory=lambda: str(uuid4()))

    subject: str = Field(min_length=1)

    predicate: str = Field(min_length=1)

    value: str = Field(min_length=1)

    content: str = Field(min_length=1)

    source_text: str = Field(min_length=1)

    status: MemoryStatus = MemoryStatus.ACTIVE

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )