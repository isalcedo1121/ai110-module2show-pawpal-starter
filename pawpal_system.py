"""PawPal+ core classes (Phase 1 skeletons, based on diagrams/uml_draft.md)."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Task:
    """A single pet care activity, such as a feeding, walk, or medication."""

    name: str
    duration: int  # minutes
    priority: str  # e.g. "low", "medium", "high"
    due_time: str  # e.g. "08:00"


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
    """Collects tasks and builds a daily care schedule from them."""

    def __init__(self) -> None:
        self.tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        """Add a task to be considered when scheduling."""
        pass

    def generate_schedule(self) -> list[Task]:
        """Return the tasks arranged into a daily plan."""
        pass
