from datetime import date, timedelta

import pawpal_system
from pawpal_system import Owner, Pet, Scheduler, Task


def make_scheduler():
    """Return a scheduler for an owner with two pets (Mochi and Luna) and no tasks."""
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "dog", 3)
    luna = Pet("Luna", "cat", 5)
    owner.add_pet(mochi)
    owner.add_pet(luna)
    return Scheduler(owner), mochi, luna


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


def test_sort_by_time_orders_chronologically():
    scheduler, _, _ = make_scheduler()
    evening = Task("Evening fetch", duration=20, priority=1, due_time="18:00")
    feeding = Task("Feeding", duration=10, priority=3, due_time="07:30")
    meds = Task("Give medication", duration=5, priority=2, due_time="09:00")
    tasks = [evening, feeding, meds]

    result = scheduler.sort_by_time(tasks)

    assert [task.due_time for task in result] == ["07:30", "09:00", "18:00"]
    assert tasks == [evening, feeding, meds]  # original list is unchanged


def test_sort_by_time_puts_earlier_date_first():
    scheduler, _, _ = make_scheduler()
    today = date.today()
    tomorrow_morning = Task("Walk", duration=30, priority=3, due_time="07:00",
                            due_date=today + timedelta(days=1))
    today_evening = Task("Fetch", duration=20, priority=1, due_time="18:00", due_date=today)

    result = scheduler.sort_by_time([tomorrow_morning, today_evening])

    assert result[0] is today_evening
    assert result[1] is tomorrow_morning


def test_daily_task_creates_next_day_copy():
    scheduler, mochi, _ = make_scheduler()
    walk = Task("Morning walk", duration=30, priority=3, due_time="08:00", frequency="daily")
    mochi.add_task(walk)

    next_walk = scheduler.mark_task_complete(walk)

    assert walk.completed is True
    assert next_walk is not None
    assert next_walk.due_date == date.today() + timedelta(days=1)
    assert next_walk.completed is False
    assert (next_walk.name, next_walk.duration, next_walk.priority, next_walk.due_time) == (
        "Morning walk", 30, 3, "08:00"
    )
    assert next_walk.frequency == "daily"
    assert len(mochi.tasks) == 2


def test_weekly_task_repeats_after_seven_days():
    scheduler, mochi, _ = make_scheduler()
    bath = Task("Bath", duration=15, priority=1, due_time="16:00", frequency="weekly")
    mochi.add_task(bath)

    next_bath = scheduler.mark_task_complete(bath)

    assert next_bath.due_date == date.today() + timedelta(days=7)
    assert next_bath.completed is False


def test_completing_twice_does_not_duplicate():
    scheduler, mochi, _ = make_scheduler()
    walk = Task("Morning walk", duration=30, priority=3, due_time="08:00", frequency="daily")
    mochi.add_task(walk)

    scheduler.mark_task_complete(walk)
    second = scheduler.mark_task_complete(walk)

    assert second is None
    assert len(mochi.tasks) == 2  # the original plus one replacement


def test_completing_again_on_next_day_does_not_duplicate(monkeypatch):
    initial_date = date(2026, 10, 18)

    class MockDate(date):
        current = initial_date

        @classmethod
        def today(cls):
            return cls.current

    monkeypatch.setattr(pawpal_system, "date", MockDate)
    scheduler, mochi, _ = make_scheduler()
    walk = Task("Morning walk", duration=30, priority=3, due_time="08:00",
                frequency="daily", due_date=initial_date)
    mochi.add_task(walk)

    next_walk = scheduler.mark_task_complete(walk)

    assert walk.completed is True
    assert next_walk is not None
    assert next_walk.due_date == initial_date + timedelta(days=1)
    assert next_walk.completed is False
    assert len(mochi.tasks) == 2

    MockDate.current = initial_date + timedelta(days=1)
    second = scheduler.mark_task_complete(walk)

    assert second is None
    assert mochi.tasks == [walk, next_walk]
    assert next_walk.completed is False


def test_detect_conflicts_flags_identical_date_and_time():
    scheduler, mochi, luna = make_scheduler()
    walk = Task("Morning walk", duration=30, priority=3, due_time="08:00")
    play = Task("Play time", duration=15, priority=2, due_time="08:00")
    mochi.add_task(walk)
    luna.add_task(play)

    warnings = scheduler.detect_conflicts([walk, play])

    assert len(warnings) == 1
    assert str(date.today()) in warnings[0]
    assert "08:00" in warnings[0]
    assert "Morning walk (Mochi)" in warnings[0]
    assert "Play time (Luna)" in warnings[0]


def test_detect_conflicts_ignores_same_time_on_different_dates():
    scheduler, mochi, _ = make_scheduler()
    today_walk = Task("Morning walk", duration=30, priority=3, due_time="08:00")
    tomorrow_walk = Task("Morning walk", duration=30, priority=3, due_time="08:00",
                         due_date=date.today() + timedelta(days=1))
    mochi.add_task(today_walk)
    mochi.add_task(tomorrow_walk)

    assert scheduler.detect_conflicts([today_walk, tomorrow_walk]) == []


def test_pet_with_no_tasks():
    scheduler, mochi, _ = make_scheduler()

    assert mochi.tasks == []
    assert scheduler.filter_tasks(pet_name="Mochi") == []
    assert scheduler.generate_schedule(available_minutes=60) == []
    assert scheduler.detect_conflicts(scheduler.filter_tasks(pet_name="Mochi")) == []
