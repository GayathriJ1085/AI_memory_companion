from core.memory.models import Memory, MemoryStatus


def test_memory_creation():

    memory = Memory(
        subject="user",
        predicate="likes",
        value="tea",
        content="User likes tea",
        source_text="I like tea.",
    )

    assert memory.subject == "user"
    assert memory.predicate == "likes"
    assert memory.value == "tea"
    assert memory.status == MemoryStatus.ACTIVE


def test_memory_gets_unique_id():

    memory1 = Memory(
        subject="user",
        predicate="likes",
        value="tea",
        content="User likes tea",
        source_text="I like tea.",
    )

    memory2 = Memory(
        subject="user",
        predicate="likes",
        value="coffee",
        content="User likes coffee",
        source_text="I like coffee.",
    )

    assert memory1.id != memory2.id


def test_memory_status_can_change():

    memory = Memory(
        subject="user",
        predicate="likes",
        value="tea",
        content="User likes tea",
        source_text="I like tea.",
    )

    memory.status = MemoryStatus.SUPERSEDED

    assert memory.status == MemoryStatus.SUPERSEDED