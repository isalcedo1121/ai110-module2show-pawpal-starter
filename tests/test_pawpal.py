from pawpal_system import Pet, Task


def test_task_completion():
    task = Task("Morning walk", duration=30, priority=3, due_time="08:00")
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_task_addition():
    pet = Pet("Mochi", "dog", 3)
    initial_count = len(pet.tasks)

    pet.add_task(Task("Feeding", duration=10, priority=3, due_time="07:30"))

    assert len(pet.tasks) == initial_count + 1
