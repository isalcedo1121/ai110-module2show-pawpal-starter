"""PawPal+ core classes (based on diagrams/uml_draft.md)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta

# How many days until a recurring task comes back. Frequencies not listed don't repeat.
RECURRENCE_DAYS = {"daily": 1, "weekly": 7}


@dataclass
class Task:
    """A single pet care activity, such as a feeding, walk, or medication."""

    name: str  # short description, e.g. "Morning walk"
    duration: int  # minutes
    priority: int  # higher number = higher priority (e.g. 1 = low, 3 = high)
    due_time: str  # 24-hour "HH:MM" format, e.g. "08:00"
    frequency: str = "daily"  # e.g. "daily", "weekly", "once"
    completed: bool = False
    due_date: date = field(default_factory=date.today)

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

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return a new list of tasks ordered by due_date, then due_time (earliest first)."""
        return sorted(tasks, key=lambda task: (task.due_date, task.due_time))

    def filter_tasks(
        self, pet_name: str | None = None, completed: bool | None = None
    ) -> list[Task]:
        """Return the owner's tasks, optionally limited to one pet and/or a completion status.

        Leave a filter as None to skip it. Pet names match case-insensitively.
        """
        matches: list[Task] = []
        for task in self.owner.get_all_tasks():
            if completed is not None and task.completed != completed:
                continue
            if pet_name is not None:
                pet = self._pet_for(task)
                if pet is None or pet.name.lower() != pet_name.lower():
                    continue
            matches.append(task)
        return matches

    def _pet_for(self, task: Task) -> Pet | None:
        """Return the pet that holds this exact task object, or None."""
        for pet in self.owner.pets:
            if any(existing is task for existing in pet.tasks):
                return pet
        return None

    def mark_task_complete(self, task: Task) -> Task | None:
        """Mark a task done and, if it repeats, add its next occurrence to the same pet.

        Returns the new task, or None if the task is already complete, doesn't
        repeat, or its next occurrence already exists.
        """
        pet = self._pet_for(task)
        if pet is None:
            raise ValueError(f"Task '{task.name}' does not belong to any of {self.owner.name}'s pets.")

        if task.completed:
            return None

        task.mark_complete()

        interval = RECURRENCE_DAYS.get(task.frequency.lower())
        if interval is None:
            return None

        # Count from today if the task was overdue, so the next one isn't already late.
        next_date = max(task.due_date, date.today()) + timedelta(days=interval)
        already_exists = any(
            existing.name == task.name
            and existing.due_time == task.due_time
            and existing.due_date == next_date
            for existing in pet.tasks
        )
        if already_exists:
            return None

        next_task = Task(
            name=task.name,
            duration=task.duration,
            priority=task.priority,
            due_time=task.due_time,
            frequency=task.frequency,
            due_date=next_date,
        )
        pet.add_task(next_task)
        return next_task

    def detect_conflicts(self, tasks: list[Task]) -> list[str]:
        """Return a warning for each date and time shared by more than one task (empty if none).

        Only exact due_date + due_time matches count; overlapping durations are not checked.
        """
        tasks_by_slot: dict[tuple[date, str], list[Task]] = {}
        for task in tasks:
            tasks_by_slot.setdefault((task.due_date, task.due_time), []).append(task)

        warnings: list[str] = []
        for (due_date, due_time), slot_tasks in sorted(tasks_by_slot.items()):
            if len(slot_tasks) < 2:
                continue
            labels = []
            for task in slot_tasks:
                pet = self._pet_for(task)
                labels.append(f"{task.name} ({pet.name})" if pet else task.name)
            warnings.append(f"Conflict on {due_date} at {due_time}: {', '.join(labels)}")
        return warnings

    def generate_schedule(self, available_minutes: int) -> list[Task]:
        """Return today's incomplete tasks that fit within available_minutes.

        Tasks due on a later date are left out; overdue tasks are included.
        Tasks are chosen highest priority first (earlier due_time breaks ties),
        skipping any task that no longer fits. The chosen tasks are returned
        in due_time order so the plan reads like a daily timeline.
        """
        today = date.today()
        pending = [task for task in self.filter_tasks(completed=False) if task.due_date <= today]
        by_importance = sorted(pending, key=lambda task: (-task.priority, task.due_time))

        chosen: list[Task] = []
        minutes_left = available_minutes
        for task in by_importance:
            if task.duration <= minutes_left:
                chosen.append(task)
                minutes_left -= task.duration

        return self.sort_by_time(chosen)
