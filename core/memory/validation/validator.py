from core.memory.extraction.schemas import MemoryCandidate
from core.memory.validation.models import (
    ValidationDecision,
    ValidationResult,
)
from core.memory.validation.rules import (
    basic_candidate_checks,
    contains_hypothetical,
    contains_negation,
    contains_uncertainty,
)


class MemoryValidator:
    """
    Validates extracted memory candidates before they can move
    further through the memory pipeline.

    The validator does NOT save memories.

    It checks whether the candidate has enough evidence to be
    considered safe.
    """

    def validate(
        self,
        candidate: MemoryCandidate,
    ) -> ValidationResult:

        is_valid, reason = basic_candidate_checks(candidate)

        if not is_valid:
            return ValidationResult(
                decision=ValidationDecision.INVALID,
                reason=reason,
            )

        source_text = candidate.source_text

        # Uncertain statements should never become confirmed
        # memories automatically.
        if contains_uncertainty(source_text):

            return ValidationResult(
                decision=ValidationDecision.REVIEW,
                reason=(
                    "Source text contains uncertainty. "
                    "Human or additional evidence review is required."
                ),
            )

        # Hypothetical statements describe possibilities rather
        # than established facts.
        if contains_hypothetical(source_text):

            return ValidationResult(
                decision=ValidationDecision.REVIEW,
                reason=(
                    "Source text appears hypothetical or future-oriented."
                ),
            )

        # A negated statement may mean the candidate is the
        # opposite of what the user actually said.
        if contains_negation(source_text):

            return ValidationResult(
                decision=ValidationDecision.REVIEW,
                reason=(
                    "Source text contains negation. "
                    "Candidate requires semantic verification."
                ),
            )

        return ValidationResult(
            decision=ValidationDecision.VALID,
            reason=(
                "Candidate has valid fields and no obvious "
                "uncertainty, hypothetical, or negation markers."
            ),
        )