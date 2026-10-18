# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🧩 Implementation Summary

The scheduling logic lives in `pawpal_system.py`, and `main.py` runs a small terminal demo of it. The system is built from four classes:

- **Task**: one care activity (for example a walk or a feeding). It has a description (`name`), a `duration` in minutes, a `priority` (higher number = more important), a `due_time` in `HH:MM` format, a `frequency`, and a `completed` flag set by `mark_complete()`.
- **Pet**: a pet's details (name, species, age) plus its own list of tasks, managed with `add_task()` and `remove_task()`.
- **Owner**: keeps a list of pets (`add_pet()`, `remove_pet()`) and gathers every pet's tasks into one list with `get_all_tasks()`.
- **Scheduler**: is created with an `Owner`. `generate_schedule(available_minutes)` asks the owner for all tasks, drops completed ones, and picks tasks highest priority first (earlier time breaks ties), skipping any that would go over the available minutes. It returns the chosen tasks in time order.

How they work together: an **Owner** has many **Pets**, and each **Pet** has many **Tasks**. The **Scheduler** keeps no task list of its own. It reads tasks through the Owner each time, so the plan always matches the pets' current tasks.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

Output of `python main.py` (60 available minutes):

```text
Today's Schedule
----------------
07:30  Feeding (10 min) [priority: 3]
08:00  Morning walk (30 min) [priority: 3]
09:00  Give medication (5 min) [priority: 2]
```

The scheduler picks tasks by priority (higher number first) and skips any task that would go over the available time. Here the three highest-priority tasks use 45 of the 60 minutes, so the 20-minute, priority-1 "Evening fetch" is left out. The chosen tasks are then listed in time order.

## 🧪 Testing PawPal+

Run the test suite from the project root (with the virtual environment activated):

```bash
python -m pytest
```

```bash
# Run the full test suite:
pytest
```

The automated tests in `tests/test_pawpal.py` cover:

- **Basics:** marking a task complete and adding a task to a pet.
- **Sorting:** `sort_by_time()` orders tasks by time and puts earlier dates first, without changing the original list.
- **Recurrence:** completing a daily task creates an incomplete copy due tomorrow, weekly tasks repeat after 7 days, and completing the same task twice does not create a duplicate.
- **Conflict detection:** two tasks at the same date and time produce one warning naming both tasks and pets, while the same time on different dates produces none.
- **Edge case:** a pet with no tasks returns empty results from filtering, scheduling, and conflict detection without errors.

Dates in the tests are calculated from `date.today()`, so they pass on any day.

Sample test output:

```text
============================= test session starts ==============================
platform darwin -- Python 3.14.6, pytest-9.1.1, pluggy-1.7.0
rootdir: /Users/ivansalcedo/repos/ai110-module2show-pawpal-starter
plugins: anyio-4.15.1
collected 10 items

tests/test_pawpal.py ..........                                          [100%]

============================== 10 passed in 0.01s ==============================
```

**Confidence Level: ⭐⭐⭐⭐☆ (4/5)**

All 10 automated tests pass, including sorting, recurrence, and conflict detection. However, some scheduling behaviors (such as priority selection under the time limit and leaving out completed or future tasks) and the Streamlit UI have not been thoroughly tested yet.

## 📐 Smarter Scheduling

All scheduling logic lives in the `Scheduler` class in `pawpal_system.py`, and each feature is demonstrated in `main.py`.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Returns a new list ordered by `due_date`, then `due_time` (earliest first), using `sorted()` with a lambda key. `HH:MM` strings sort correctly because they are zero-padded. The original list is not changed. |
| Filtering | `Scheduler.filter_tasks()` | Filters by pet name (case-insensitive), by completion status, or both. Either filter can be left out. Reads tasks through `Owner` → `Pet` instead of keeping a separate task list. |
| Daily plan | `Scheduler.generate_schedule()` | Uses only incomplete tasks due today or earlier (future tasks are left out). Picks the highest priority first, with earlier time breaking ties, and skips any task that would go over `available_minutes`. Returns the plan sorted by time. |
| Conflict handling | `Scheduler.detect_conflicts()` | Groups tasks by `(due_date, due_time)` and returns a warning such as `Conflict on 2026-10-18 at 08:00: Morning walk (Mochi), Play time (Luna)` for each slot with more than one task, for the same pet or different pets. Returns an empty list when there are no conflicts and never raises an error or removes tasks. **Only exact date/time matches are detected; overlapping durations are not** (e.g., a 30-minute task at 08:00 and another at 08:15 are not flagged). |
| Recurring tasks | `Scheduler.mark_task_complete()` | Marks the task done. If it is `"daily"` or `"weekly"`, adds a new incomplete copy to the same pet due 1 or 7 days later (using `timedelta`). `"once"` tasks do not repeat. Completing the same task twice does not create a duplicate. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
