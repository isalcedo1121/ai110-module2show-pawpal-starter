"""PawPal+ core classes (Phase 1 skeletons, based on diagrams/uml_draft.md)."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Task:
    """A single pet care activity, such as a feeding, walk, or medication."""

    name: str
    duration: int  # minutes
    priority: int  # higher number = higher priority (e.g. 1 = low, 3 = high)
    due_time: str  # 24-hour "HH:MM" format, e.g. "08:00"


@dataclass
class Pet:
    """A pet and the care tasks that belong to it."""

    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet."""
        pass

    def remove_task(self, task: Task) -> None:
        """Remove a care task from this pet."""
        pass


class Owner:
    """A pet owner who manages one or more pets."""

    def __init__(self, name: str) -> None:
        self.name: str = name
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        pass

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner."""
        pass


class Scheduler:
    """Builds a daily care schedule from the tasks of an owner's pets."""

    def __init__(self, owner: Owner) -> None:
        self.owner: Owner = owner

    def generate_schedule(self, available_minutes: int) -> list[Task]:
        """Return tasks gathered from owner.pets, arranged into a daily plan
        that fits within available_minutes."""
        pass
