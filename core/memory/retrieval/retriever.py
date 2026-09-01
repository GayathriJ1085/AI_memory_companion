from collections.abc import Iterable
import re

from core.memory.models import Memory, MemoryStatus
from core.memory.retrieval.models import (
    RetrievedMemory,
    RetrievalQuery,
    RetrievalResult,
)


class MemoryRetriever:
    """
    Retrieves existing memories related to a query.

    The retriever supports two kinds of matching:

    1. Structured matching
       - subject
       - predicate
       - value
       - content

    2. Natural-language keyword matching
       - useful when the user asks a conversational question
       - allows long-term memories to be recalled even when
         the query does not exactly match the stored memory

    This is still a deterministic retriever.
    It is NOT a vector database or embedding-based retriever.
    """

    def __init__(
        self,
        memories: Iterable[Memory] | None = None,
    ) -> None:

        self._memories: list[Memory] = list(memories or [])

    def add_memory(self, memory: Memory) -> None:
        """
        Add a memory to the searchable collection.
        """

        self._memories.append(memory)

    def retrieve(
        self,
        query: RetrievalQuery,
    ) -> RetrievalResult:
        """
        Find active memories related to the query.

        Memories are scored using both structured matching
        and natural-language keyword matching.
        """

        matches: list[RetrievedMemory] = []

        for memory in self._memories:

            # Only active memories should participate
            # in normal retrieval.
            if memory.status != MemoryStatus.ACTIVE:
                continue

            score = self._calculate_score(
                memory,
                query,
            )

            if score > 0:
                matches.append(
                    RetrievedMemory(
                        memory=memory,
                        score=min(score, 1.0),
                    )
                )

        # Highest-scoring memories first.
        matches.sort(
            key=lambda item: item.score,
            reverse=True,
        )

        return RetrievalResult(
            matches=matches
        )

    @staticmethod
    def _calculate_score(
        memory: Memory,
        query: RetrievalQuery,
    ) -> float:
        """
        Calculate deterministic similarity.

        Structured matching has priority.

        Weighting:

        subject   = 0.40
        predicate = 0.40
        value     = 0.10
        content   = 0.10

        Natural-language keyword matching is only used when
        structured fields are not sufficient.
        """

        score = 0.0

        # --------------------------------------------------
        # 1. Structured matching
        # --------------------------------------------------

        if (
            query.subject is not None
            and memory.subject.lower() == query.subject.lower()
        ):
            score += 0.40

        if (
            query.predicate is not None
            and memory.predicate.lower() == query.predicate.lower()
        ):
            score += 0.40

        if (
            query.value is not None
            and memory.value.lower() == query.value.lower()
        ):
            score += 0.10

        if (
            query.content is not None
            and memory.content.lower() == query.content.lower()
        ):
            score += 0.10

        # --------------------------------------------------
        # 2. Natural-language matching
        # --------------------------------------------------

        if query.content is not None:

            query_words = MemoryRetriever._extract_keywords(
                query.content
            )

            memory_text = " ".join(
                [
                    memory.subject,
                    memory.predicate,
                    memory.value,
                    memory.content,
                ]
            ).lower()

            memory_words = MemoryRetriever._extract_keywords(
                memory_text
            )

            if query_words and memory_words:

                matching_words = (
                    query_words & memory_words
                )

                keyword_ratio = (
                    len(matching_words)
                    / len(query_words)
                )

                # Small additional score so keyword matching
                # can discover memories without overpowering
                # exact structured matches.
                score += 0.20 * keyword_ratio

        return score

    @staticmethod
    def _extract_keywords(text: str) -> set[str]:
        """
        Extract useful words from natural language.

        Common conversational stop words are ignored.
        """

        words = re.findall(
            r"[a-zA-Z0-9]+",
            text.lower(),
        )

        stop_words = {
            "a",
            "an",
            "and",
            "are",
            "am",
            "be",
            "been",
            "being",
            "do",
            "does",
            "did",
            "for",
            "from",
            "i",
            "im",
            "in",
            "is",
            "it",
            "me",
            "my",
            "of",
            "on",
            "or",
            "that",
            "the",
            "this",
            "to",
            "was",
            "we",
            "what",
            "when",
            "where",
            "which",
            "who",
            "why",
            "with",
            "you",
            "your",
        }

        return {
            word
            for word in words
            if word not in stop_words
            and len(word) > 1
        }