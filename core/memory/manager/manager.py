from core.memory.conflict.detector import ConflictDetector
from core.memory.extraction.extractor import MemoryExtractor
from core.memory.extraction.schemas import MemoryCandidate
from core.memory.models import Memory, MemoryStatus
from core.memory.relevance.models import RelevanceDecision
from core.memory.relevance.scorer import RelevanceScorer
from core.memory.retrieval.query import query_from_candidate
from core.memory.retrieval.retriever import MemoryRetriever
from core.memory.storage.repository import MemoryRepository
from core.memory.validation.models import ValidationDecision
from core.memory.validation.validator import MemoryValidator


class MemoryManager:
    """
    Coordinates the complete memory-processing pipeline.

    Pipeline:

        user message
            ↓
        extraction
            ↓
        candidate
            ↓
        relevance
            ↓
        validation
            ↓
        retrieval
            ↓
        conflict detection
            ↓
        storage
    """

    def __init__(
        self,
        extractor: MemoryExtractor,
        relevance_scorer: RelevanceScorer,
        validator: MemoryValidator,
        repository: MemoryRepository,
        retriever: MemoryRetriever,
        conflict_detector: ConflictDetector,
    ) -> None:

        self.extractor = extractor
        self.relevance_scorer = relevance_scorer
        self.validator = validator
        self.repository = repository
        self.retriever = retriever
        self.conflict_detector = conflict_detector

    def process_message(
        self,
        user_message: str,
    ) -> list[str]:
        """
        Extract and process all memory candidates
        from a user message.

        Returns one result for each extracted candidate.
        """

        extraction_result = self.extractor.extract(
            user_message
        )

        results = []

        for candidate in extraction_result.candidates:
            result = self.process_candidate(candidate)
            results.append(result)

        return results

    def get_relevant_memories(
        self,
        user_message: str,
        limit: int = 5,
    ) -> list[Memory]:
        """
        Retrieve active long-term memories that may be
        relevant to the current user message.

        The current implementation uses deterministic
        lexical matching.

        This can later be replaced with semantic/vector
        retrieval without changing the rest of the system.
        """

        if not user_message or not user_message.strip():
            return []

        query_text = user_message.lower()

        active_memories = self.repository.list_active()

        scored_memories: list[tuple[float, Memory]] = []

        for memory in active_memories:

            score = 0.0

            memory_text = (
                f"{memory.subject} "
                f"{memory.predicate} "
                f"{memory.value} "
                f"{memory.content}"
            ).lower()

            # --------------------------------------------------
            # 1. Word overlap
            # --------------------------------------------------

            query_words = set(
                query_text
                .replace("?", "")
                .replace(".", "")
                .replace(",", "")
                .split()
            )

            memory_words = set(
                memory_text
                .replace("?", "")
                .replace(".", "")
                .replace(",", "")
                .split()
            )

            overlap = query_words.intersection(
                memory_words
            )

            if overlap:
                score += min(
                    len(overlap) * 0.10,
                    0.40,
                )

            # --------------------------------------------------
            # 2. Predicate matching
            # --------------------------------------------------

            predicate = memory.predicate.lower()

            predicate_aliases = {
                "likes": [
                    "like",
                    "likes",
                    "liked",
                    "enjoy",
                    "enjoys",
                    "favorite",
                    "favourite",
                ],
                "dislikes": [
                    "dislike",
                    "dislikes",
                    "hate",
                    "hates",
                    "avoid",
                    "avoids",
                ],
                "lives_in": [
                    "live",
                    "lives",
                    "living",
                    "reside",
                    "resides",
                    "home",
                ],
                "goes_for_walk": [
                    "walk",
                    "walks",
                    "walking",
                ],
            }

            aliases = predicate_aliases.get(
                predicate,
                [predicate],
            )

            if any(
                alias in query_text
                for alias in aliases
            ):
                score += 0.40

            # --------------------------------------------------
            # 3. User-specific memory
            # --------------------------------------------------

            if memory.subject.lower() == "user":
                score += 0.20

            # --------------------------------------------------
            # 4. Only return memories with some relevance
            # --------------------------------------------------

            if score > 0:
                scored_memories.append(
                    (score, memory)
                )

        # Highest relevance first.
        scored_memories.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            memory
            for _, memory in scored_memories[:limit]
        ]

    def process_candidate(
        self,
        candidate: MemoryCandidate,
    ) -> str:
        """
        Process one memory candidate.

        Returns:
            STORED
            REJECTED
            REVIEW
            SUPERSEDED_AND_STORED
        """

        # --------------------------------------------------
        # 1. Relevance
        # --------------------------------------------------

        relevance = self.relevance_scorer.score(
            candidate
        )

        if relevance.decision == RelevanceDecision.REJECT:
            return "REJECTED"

        if relevance.decision == RelevanceDecision.REVIEW:
            return "REVIEW"

        # --------------------------------------------------
        # 2. Validation
        # --------------------------------------------------

        validation = self.validator.validate(
            candidate
        )

        if validation.decision == ValidationDecision.INVALID:
            return "REJECTED"

        if validation.decision == ValidationDecision.REVIEW:
            return "REVIEW"

        # --------------------------------------------------
        # 3. Retrieve related active memories
        # --------------------------------------------------

        query = query_from_candidate(
            candidate
        )

        retrieval_result = self.retriever.retrieve(
            query
        )

        had_conflict = False

        # --------------------------------------------------
        # 4. Detect conflicts
        # --------------------------------------------------

        for retrieved in retrieval_result.matches:

            existing_memory = retrieved.memory

            conflict = self.conflict_detector.detect(
                candidate,
                existing_memory,
            )

            if conflict.decision.value == "CONFLICT":

                had_conflict = True

                self.repository.supersede(
                    existing_memory.id
                )

        # --------------------------------------------------
        # 5. Convert candidate into trusted memory
        # --------------------------------------------------

        memory = Memory(
            subject=candidate.subject,
            predicate=candidate.predicate,
            value=candidate.value,
            content=candidate.content,
            source_text=candidate.source_text,
            status=MemoryStatus.ACTIVE,
        )

        # --------------------------------------------------
        # 6. Store
        # --------------------------------------------------

        self.repository.add(
            memory
        )

        # Keep retrieval collection synchronized.
        self.retriever.add_memory(
            memory
        )

        if had_conflict:
            return "SUPERSEDED_AND_STORED"

        return "STORED"