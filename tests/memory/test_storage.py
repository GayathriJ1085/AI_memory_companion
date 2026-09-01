import pytest

from core.memory.models import Memory, MemoryStatus
from core.memory.storage.repository import MemoryRepository


def make_memory(value: str = "tea") -> Memory:
    return Memory(
        subject="user",
        predicate="likes",
        value=value,
        content=f"User likes {value}",
        source_text=f"I like {value}.",
    )


def test_add_and_get_memory():
    repository = MemoryRepository()
    memory = make_memory()

    repository.add(memory)

    result = repository.get(memory.id)

    assert result is not None
    assert result.id == memory.id
    assert result.value == "tea"


def test_get_unknown_memory_returns_none():
    repository = MemoryRepository()

    assert repository.get("does-not-exist") is None


def test_list_all_returns_all_memories():
    repository = MemoryRepository()

    memory1 = make_memory("tea")
    memory2 = make_memory("coffee")

    repository.add(memory1)
    repository.add(memory2)

    result = repository.list_all()

    assert len(result) == 2
    assert memory1 in result
    assert memory2 in result


def test_list_active_returns_only_active_memories():
    repository = MemoryRepository()

    active_memory = make_memory("tea")
    superseded_memory = make_memory("coffee")

    superseded_memory.status = MemoryStatus.SUPERSEDED

    repository.add(active_memory)
    repository.add(superseded_memory)

    result = repository.list_active()

    assert len(result) == 1
    assert result[0].id == active_memory.id


def test_update_memory():
    repository = MemoryRepository()

    memory = make_memory("tea")
    repository.add(memory)

    memory.value = "coffee"
    memory.content = "User likes coffee"

    repository.update(memory)

    result = repository.get(memory.id)

    assert result is not None
    assert result.value == "coffee"


def test_supersede_memory():
    repository = MemoryRepository()

    memory = make_memory("tea")
    repository.add(memory)

    result = repository.supersede(memory.id)

    assert result.status == MemoryStatus.SUPERSEDED


def test_superseded_memory_is_not_active():
    repository = MemoryRepository()

    memory = make_memory("tea")
    repository.add(memory)

    repository.supersede(memory.id)

    assert repository.list_active() == []


def test_duplicate_memory_is_rejected():
    repository = MemoryRepository()

    memory = make_memory()

    repository.add(memory)

    with pytest.raises(ValueError):
        repository.add(memory)


def test_updating_unknown_memory_is_rejected():
    repository = MemoryRepository()

    memory = make_memory()

    with pytest.raises(KeyError):
        repository.update(memory)


def test_superseding_unknown_memory_is_rejected():
    repository = MemoryRepository()

    with pytest.raises(KeyError):
        repository.supersede("does-not-exist")


def test_delete_memory():
    repository = MemoryRepository()

    memory = make_memory()
    repository.add(memory)

    repository.delete(memory.id)

    assert repository.get(memory.id) is None


def test_clear_repository():
    repository = MemoryRepository()

    repository.add(make_memory("tea"))
    repository.add(make_memory("coffee"))

    repository.clear()

    assert repository.list_all() == []
