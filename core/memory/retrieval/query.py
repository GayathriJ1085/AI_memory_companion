from core.memory.extraction.schemas import MemoryCandidate
from core.memory.retrieval.models import RetrievalQuery


def query_from_candidate(
    candidate: MemoryCandidate,
) -> RetrievalQuery:
    """
    Convert a memory candidate into a retrieval query.

    Used by the memory-processing pipeline when checking
    whether a candidate conflicts with existing memories.
    """

    return RetrievalQuery(
        subject=candidate.subject,
        predicate=candidate.predicate,
        value=candidate.value,
        content=candidate.content,
    )


def query_from_message(
    user_message: str,
) -> RetrievalQuery:
    """
    Convert a normal conversational user message into a
    retrieval query.

    Unlike query_from_candidate(), we do not know the
    subject, predicate, or value yet.

    The natural-language message is therefore placed in
    the content field so that MemoryRetriever can use
    keyword matching.
    """

    return RetrievalQuery(
        content=user_message.strip(),
    )