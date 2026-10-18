"""Demo script: build a sample owner, pets, and tasks, then print today's schedule."""

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner("Ivan")

    mochi = Pet("Mochi", "dog", 3)
    luna = Pet("Luna", "cat", 5)

    mochi.add_task(Task("Morning walk", duration=30, priority=3, due_time="08:00"))
    mochi.add_task(Task("Evening fetch", duration=20, priority=1, due_time="18:00"))
    luna.add_task(Task("Feeding", duration=10, priority=3, due_time="07:30"))
    luna.add_task(Task("Give medication", duration=5, priority=2, due_time="09:00"))

    owner.add_pet(mochi)
    owner.add_pet(luna)

    scheduler = Scheduler(owner)
    schedule = scheduler.generate_schedule(available_minutes=60)

    print("Today's Schedule")
    print("-" * 16)
    for task in schedule:
        print(f"{task.due_time}  {task.name} ({task.duration} min) [priority: {task.priority}]")


if __name__ == "__main__":
    main()
