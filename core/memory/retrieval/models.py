from pydantic import BaseModel, Field

from core.memory.models import Memory


class RetrievalQuery(BaseModel):
    """
    Describes what we are looking for in existing memories.
    """

    subject: str | None = None
    predicate: str | None = None
    value: str | None = None
    content: str | None = None


class RetrievedMemory(BaseModel):
    """
    A memory returned by the retrieval layer together with
    a deterministic relevance score.
    """

    memory: Memory

    score: float = Field(ge=0.0, le=1.0)


class RetrievalResult(BaseModel):
    """
    Collection of memories related to a retrieval query.
    """

    matches: list[RetrievedMemory]