from core.memory.extraction.schemas import MemoryCandidate
from core.memory.relevance.models import (
    RelevanceDecision,
    RelevanceResult,
)
from core.memory.relevance.rules import calculate_rule_score


class RelevanceScorer:
    """
    Determines whether an extracted memory candidate is worth
    keeping as a potential long-term memory.

    Current version uses deterministic rules only.

    AI-based semantic evaluation can be added later for ambiguous
    candidates.
    """

    ACCEPT_THRESHOLD = 0.75
    REJECT_THRESHOLD = 0.30

    def score(
        self,
        candidate: MemoryCandidate,
    ) -> RelevanceResult:

        score = calculate_rule_score(candidate)

        if score >= self.ACCEPT_THRESHOLD:
            decision = RelevanceDecision.ACCEPT
            reason = "Candidate appears useful for long-term personalization."

        elif score <= self.REJECT_THRESHOLD:
            decision = RelevanceDecision.REJECT
            reason = "Candidate appears too temporary or insufficiently useful."

        else:
            decision = RelevanceDecision.REVIEW
            reason = "Candidate has ambiguous long-term relevance and requires review."

        return RelevanceResult(
            decision=decision,
            score=score,
            reason=reason,
        )