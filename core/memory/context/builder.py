from core.memory.models import Memory


class MemoryContextBuilder:
    """
    Converts stored long-term memories into context
    that can be supplied to the conversational AI.
    """

    def build(
        self,
        memories: list[Memory],
    ) -> str:
        """
        Build a concise long-term memory context.

        If there are no relevant memories, return an empty string.
        """

        if not memories:
            return ""

        lines = [
            "LONG-TERM MEMORY",
            "The following information was previously provided by the user.",
            "Use it only when relevant to the current conversation.",
            "Do not invent information beyond these memories.",
            "",
        ]

        for memory in memories:
            lines.append(
                f"- {memory.content}"
            )

        return "\n".join(lines)