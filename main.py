"""Demo script: build a sample owner, pets, and tasks, then print today's schedule."""

from pawpal_system import Owner, Pet, Scheduler, Task


def print_tasks(title: str, tasks: list[Task]) -> None:
    """Print a heading followed by one line per task."""
    print(title)
    print("-" * len(title))
    for task in tasks:
        status = "done" if task.completed else "todo"
        print(
            f"{task.due_date} {task.due_time}  {task.name} ({task.duration} min) "
            f"[priority: {task.priority}] [{task.frequency}] [{status}]"
        )
    print()


def print_schedule(schedule: list[Task]) -> None:
    """Print the daily plan under a "Today's Schedule" heading."""
    print("Today's Schedule")
    print("-" * 16)
    for task in schedule:
        print(f"{task.due_time}  {task.name} ({task.duration} min) [priority: {task.priority}]")
    print()


def print_warnings(title: str, warnings: list[str]) -> None:
    """Print conflict warnings, or a note that there are none."""
    print(f"{title}:")
    if not warnings:
        print("  No conflicts found.")
    for warning in warnings:
        print(f"  WARNING: {warning}")
    print()


def main() -> None:
    owner = Owner("Ivan")

    mochi = Pet("Mochi", "dog", 3)
    luna = Pet("Luna", "cat", 5)

    # Tasks are added out of time order on purpose to show sorting.
    mochi.add_task(Task("Evening fetch", duration=20, priority=1, due_time="18:00"))
    luna.add_task(Task("Give medication", duration=5, priority=2, due_time="09:00"))
    mochi.add_task(Task("Morning walk", duration=30, priority=3, due_time="08:00"))
    luna.add_task(Task("Feeding", duration=10, priority=3, due_time="07:30"))

    litter = Task("Clean litter box", duration=10, priority=2, due_time="06:45")
    luna.add_task(litter)
    litter.mark_complete()  # already done today, so it's left out of the schedule

    owner.add_pet(mochi)
    owner.add_pet(luna)

    scheduler = Scheduler(owner)

    all_tasks = owner.get_all_tasks()
    print_tasks("All tasks (as added)", all_tasks)
    print_tasks("All tasks (sorted by time)", scheduler.sort_by_time(all_tasks))
    print_tasks("Mochi's tasks", scheduler.sort_by_time(scheduler.filter_tasks(pet_name="Mochi")))
    print_tasks("Completed tasks", scheduler.filter_tasks(completed=True))
    print_tasks("Incomplete tasks", scheduler.sort_by_time(scheduler.filter_tasks(completed=False)))

    print_schedule(scheduler.generate_schedule(available_minutes=60))

    # --- Recurring tasks ---
    print("=== Recurring tasks ===\n")

    # Daily: completing Feeding adds tomorrow's Feeding to Luna.
    feeding = next(task for task in luna.tasks if task.name == "Feeding")
    next_feeding = scheduler.mark_task_complete(feeding)
    print(f"Completed daily '{feeding.name}' ({feeding.due_date}) -> next one due {next_feeding.due_date}")

    # Completing the same task again does not add a second copy.
    again = scheduler.mark_task_complete(feeding)
    feeding_count = sum(1 for task in luna.tasks if task.name == "Feeding")
    print(f"Completed it again -> new task: {again}, Feeding tasks for Luna: {feeding_count}")

    # Weekly: a bath comes back 7 days later.
    bath = Task("Bath", duration=15, priority=1, due_time="16:00", frequency="weekly")
    mochi.add_task(bath)
    next_bath = scheduler.mark_task_complete(bath)
    print(f"Completed weekly '{bath.name}' ({bath.due_date}) -> next one due {next_bath.due_date}")

    # One-time: a vet visit does not repeat.
    vet = Task("Vet checkup", duration=45, priority=3, due_time="11:00", frequency="once")
    mochi.add_task(vet)
    next_vet = scheduler.mark_task_complete(vet)
    print(f"Completed one-time '{vet.name}' -> next one: {next_vet}")
    print()

    print_tasks("All tasks after completions (sorted by time)", scheduler.sort_by_time(owner.get_all_tasks()))

    # Completed tasks and tomorrow's/next week's copies are left out of today's plan.
    plan = scheduler.generate_schedule(available_minutes=60)
    print_schedule(plan)

    # --- Conflict detection ---
    print("=== Conflict detection ===\n")

    # Today's plan has every task at a different time, so there are no warnings.
    print_warnings("Conflicts in today's plan", scheduler.detect_conflicts(plan))

    # Add tasks that share a time slot: one with another pet, one with the same pet.
    luna.add_task(Task("Play time", duration=15, priority=2, due_time="08:00"))  # same time as Mochi's walk
    mochi.add_task(Task("Nail trim", duration=10, priority=1, due_time="18:00"))  # same time as Mochi's fetch

    pending = scheduler.filter_tasks(completed=False)
    print_warnings("Conflicts among all incomplete tasks", scheduler.detect_conflicts(pending))


if __name__ == "__main__":
    main()
