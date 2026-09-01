from core.memory.extraction.schemas import MemoryCandidate
from core.memory.models import Memory
from core.memory.conflict.models import (
    ConflictDecision,
    ConflictResult,
)
from core.memory.conflict.rules import is_potential_conflict


class ConflictDetector:
    """
    Detects potential contradictions between a new memory candidate
    and an existing memory.

    This component does NOT:
    - delete memories
    - update memories
    - choose which memory is correct
    - save anything

    It only identifies potential conflicts.
    """

    def detect(
        self,
        candidate: MemoryCandidate,
        existing_memory: Memory,
    ) -> ConflictResult:

        if is_potential_conflict(
            candidate,
            existing_memory,
        ):
            return ConflictResult(
                decision=ConflictDecision.CONFLICT,
                reason=(
                    "Candidate and existing memory have the same "
                    "subject and predicate but different values."
                ),
                existing_memory_id=existing_memory.id,
                existing_memory=existing_memory,
            )

        return ConflictResult(
            decision=ConflictDecision.NO_CONFLICT,
            reason=(
                "Candidate and existing memory do not represent "
                "a direct structural conflict."
            ),
            existing_memory_id=existing_memory.id,
            existing_memory=existing_memory,
        )