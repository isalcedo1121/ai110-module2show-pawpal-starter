"""PawPal+ core classes (based on diagrams/uml_draft.md)."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Task:
    """A single pet care activity, such as a feeding, walk, or medication."""

    name: str  # short description, e.g. "Morning walk"
    duration: int  # minutes
    priority: int  # higher number = higher priority (e.g. 1 = low, 3 = high)
    due_time: str  # 24-hour "HH:MM" format, e.g. "08:00"
    frequency: str = "daily"  # e.g. "daily", "weekly", "once"
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True


@dataclass
class Pet:
    """A pet and the care tasks that belong to it."""

    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a care task from this pet, if it is present."""
        if task in self.tasks:
            self.tasks.remove(task)


class Owner:
    """A pet owner who manages one or more pets."""

    def __init__(self, name: str) -> None:
        """Create an owner with the given name and no pets."""
        self.name: str = name
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner, if it is present."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return every task from every pet as a single list."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    """Builds a daily care schedule from the tasks of an owner's pets."""

    def __init__(self, owner: Owner) -> None:
        """Create a scheduler that plans for the given owner's pets."""
        self.owner: Owner = owner

    def generate_schedule(self, available_minutes: int) -> list[Task]:
        """Return the incomplete tasks that fit within available_minutes.

        Tasks are chosen highest priority first (earlier due_time breaks ties),
        skipping any task that no longer fits. The chosen tasks are returned
        in due_time order so the plan reads like a daily timeline.
        """
        pending = [task for task in self.owner.get_all_tasks() if not task.completed]
        by_importance = sorted(pending, key=lambda task: (-task.priority, task.due_time))

        chosen: list[Task] = []
        minutes_left = available_minutes
        for task in by_importance:
            if task.duration <= minutes_left:
                chosen.append(task)
                minutes_left -= task.duration

        return sorted(chosen, key=lambda task: task.due_time)
