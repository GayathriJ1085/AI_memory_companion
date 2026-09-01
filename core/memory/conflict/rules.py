from core.memory.extraction.schemas import MemoryCandidate
from core.memory.models import Memory


def same_subject(
    candidate: MemoryCandidate,
    memory: Memory,
) -> bool:
    return candidate.subject.strip().lower() == memory.subject.strip().lower()


def same_predicate(
    candidate: MemoryCandidate,
    memory: Memory,
) -> bool:
    return candidate.predicate.strip().lower() == memory.predicate.strip().lower()


def same_value(
    candidate: MemoryCandidate,
    memory: Memory,
) -> bool:
    return candidate.value.strip().lower() == memory.value.strip().lower()


def is_potential_conflict(
    candidate: MemoryCandidate,
    memory: Memory,
) -> bool:
    """
    Two memories are potential conflicts when they describe
    the same subject and relationship but have different values.

    Example:

        user -> likes -> tea
        user -> likes -> coffee

    Same subject + same predicate + different value
    means they potentially conflict.
    """

    if not same_subject(candidate, memory):
        return False

    if not same_predicate(candidate, memory):
        return False

    if same_value(candidate, memory):
        return False

    return True