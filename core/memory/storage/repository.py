from core.memory.models import Memory, MemoryStatus


class MemoryRepository:
    """
    In-memory repository for storing Memory objects.
    """

    def __init__(self) -> None:
        self._memories: dict[str, Memory] = {}

    def add(self, memory: Memory) -> Memory:
        """Add a memory to the repository."""

        if memory.id in self._memories:
            raise ValueError(
                f"Memory with id '{memory.id}' already exists."
            )

        self._memories[memory.id] = memory
        return memory

    def get(self, memory_id: str) -> Memory | None:
        """Get a memory by its ID."""

        return self._memories.get(memory_id)

    def list_all(self) -> list[Memory]:
        """Return all memories."""

        return list(self._memories.values())

    def list_active(self) -> list[Memory]:
        """Return only active memories."""

        return [
            memory
            for memory in self._memories.values()
            if memory.status == MemoryStatus.ACTIVE
        ]

    def update(self, memory: Memory) -> Memory:
        """Update an existing memory."""

        if memory.id not in self._memories:
            raise KeyError(
                f"Memory with id '{memory.id}' does not exist."
            )

        self._memories[memory.id] = memory
        return memory

    def supersede(self, memory_id: str) -> Memory:
        """Mark a memory as superseded without deleting it."""

        memory = self.get(memory_id)

        if memory is None:
            raise KeyError(
                f"Memory with id '{memory_id}' does not exist."
            )

        memory.status = MemoryStatus.SUPERSEDED
        self._memories[memory.id] = memory

        return memory

    def delete(self, memory_id: str) -> None:
        """Permanently delete a memory."""

        if memory_id not in self._memories:
            raise KeyError(
                f"Memory with id '{memory_id}' does not exist."
            )

        del self._memories[memory_id]

    def clear(self) -> None:
        """Remove all memories."""

        self._memories.clear()
