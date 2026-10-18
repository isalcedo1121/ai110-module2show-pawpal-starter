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

## ✨ Features

**In the Streamlit app (`app.py`)**

- **Pets:** enter an owner name, then add pets with a name, species, and age. Duplicate pet names are rejected, and current pets are listed in a table.
- **Care tasks:** add a task to a chosen pet with a name, duration (minutes), priority (Low / Medium / High), and due time. New tasks are due today and repeat daily by default.
- **Task editing:** in **Edit Task**, select an existing task by pet, name, date, and time. Set **New duration (minutes)** and **New priority**, then click **Save changes**. This updates the original task in its pet's task list. The current task table updates immediately; click **Generate schedule** again to use the revised duration and priority. An empty task list shows guidance to add a task first.
- **Sorting and filtering:** the task list is always shown in time order (`sort_by_time()`) and can be filtered by pet and by status (To do / Done) using `filter_tasks()`.
- **Daily schedule:** set the minutes available today and click **Generate schedule**. Tasks are chosen highest priority first, any task that would go over the time limit is skipped, and the plan is shown in time order along with a separate table of skipped tasks.
- **Conflict warnings:** if two tasks share the same date and time, a yellow `st.warning` names both tasks, their pets, and the time. Conflicting tasks are kept; the owner decides what to change.

**In the backend and CLI demo only (`pawpal_system.py`, `main.py`)**

- **Marking tasks complete:** `Scheduler.mark_task_complete()` marks a task done. The app has no complete button yet, so the **Done** filter in the UI is always empty.
- **Daily and weekly recurrence:** completing a daily task creates a copy for tomorrow, a weekly task for 7 days later, and a one-time task doesn't repeat. This is shown in `main.py` and the tests, but not in the app.
- **Removing pets and tasks:** `Owner.remove_pet()` and `Pet.remove_task()` exist but aren't connected to the UI.

**Current limitations**

- Pets and tasks are stored in the browser session only and are lost when the page is refreshed.
- Tasks can't be marked complete or deleted in the app. The editor changes duration and priority only.
- Conflicts are only detected for identical date and time; overlapping durations are not detected, and conflicts are never resolved automatically.

## 🖥️ Sample Output

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

The backend tests in `tests/test_pawpal.py` cover:

- **Basics:** marking a task complete and adding a task to a pet.
- **Sorting:** `sort_by_time()` orders tasks by time and puts earlier dates first, without changing the original list.
- **Recurrence:** completing a daily task creates an incomplete copy due tomorrow, weekly tasks repeat after 7 days, and completing the same task twice does not create a duplicate, including after advancing to the next calendar day.
- **Conflict detection:** two tasks at the same date and time produce one warning naming both tasks and pets, while the same time on different dates produces none.
- **Edge case:** a pet with no tasks returns empty results from filtering, scheduling, and conflict detection without errors.

The Streamlit AppTest tests in `tests/test_app.py` cover the empty editor, updating the original Task object, duration edits changing whether a task fits the budget, priority edits changing which task is scheduled, and switching between same-named tasks for different pets without changing the wrong task. They also check that saved values survive reruns and conflict warnings remain visible.

Most tests calculate dates from `date.today()`. The cross-day recurrence regression uses pytest's built-in `monkeypatch` fixture to replace the backend's date class and simulate the next calendar day without an additional dependency.

Sample test output:

```text
============================= test session starts ==============================
platform darwin -- Python 3.14.6, pytest-9.1.1, pluggy-1.7.0
rootdir: /Users/ivansalcedo/repos/ai110-module2show-pawpal-starter
plugins: anyio-4.15.1
collected 15 items

tests/test_app.py ....                                                   [ 26%]
tests/test_pawpal.py ...........                                         [100%]

============================== 15 passed in 0.62s ==============================
```

**Confidence Level: ⭐⭐⭐⭐☆ (4/5)**

All 15 automated tests pass, covering backend sorting, recurrence, and conflict detection, plus Streamlit editing and its effects on priority selection and the time budget. The suite does not yet include dedicated tests for leaving out completed or future tasks or every Streamlit workflow. The CLI example below also provides a manual check of priority selection and time tie-breaking.

## 📐 Smarter Scheduling

All scheduling logic lives in the `Scheduler` class in `pawpal_system.py`, and each feature is demonstrated in `main.py`.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Returns a new list ordered by `due_date`, then `due_time` (earliest first), using `sorted()` with a lambda key. `HH:MM` strings sort correctly because they are zero-padded. The original list is not changed. |
| Filtering | `Scheduler.filter_tasks()` | Filters by pet name (case-insensitive), by completion status, or both. Either filter can be left out. Reads tasks through `Owner` → `Pet` instead of keeping a separate task list. |
| Daily plan | `Scheduler.generate_schedule()` | Uses only incomplete tasks due today or earlier (future tasks are left out). Picks the highest priority first, with earlier time breaking ties, and skips any task that would go over `available_minutes`. Returns the plan sorted by time. |
| Conflict handling | `Scheduler.detect_conflicts()` | Groups tasks by `(due_date, due_time)` and returns a warning such as `Conflict on 2026-10-18 at 08:00: Morning walk (Mochi), Play time (Luna)` for each slot with more than one task, for the same pet or different pets. Returns an empty list when there are no conflicts and never raises an error or removes tasks. **Only exact date/time matches are detected; overlapping durations are not** (e.g., a 30-minute task at 08:00 and another at 08:15 are not flagged). |
| Recurring tasks | `Scheduler.mark_task_complete()` | Marks the task done. If it is `"daily"` or `"weekly"`, adds a new incomplete copy to the same pet due 1 or 7 days later (using `timedelta`). `"once"` tasks do not repeat. Completing the same task twice does not create a duplicate. |

## Optional Challenge 3: Advanced Priority Scheduling

The app offers **Low**, **Medium**, and **High** priorities, mapped to `Task.priority` values **1**, **2**, and **3** by `PRIORITY_VALUES` in `app.py`. `Scheduler.generate_schedule()` selects tasks by highest priority first, then earliest due time within each priority. It skips tasks that exceed the remaining minutes and returns the selected tasks in chronological order for the daily timeline.

Run this focused example from the project root with the virtual environment activated. Each task takes 10 minutes, and the budget allows only one task:

```bash
python - <<'PY'
from pawpal_system import Owner, Pet, Scheduler, Task
from main import print_schedule

owner = Owner('Jordan')
pet = Pet('Mochi', 'dog', 3)
owner.add_pet(pet)
for name, priority, due_time in [
    ('Play', 1, '06:00'),
    ('Grooming', 2, '07:00'),
    ('Medication', 3, '09:00'),
    ('Feeding', 3, '08:00'),
]:
    pet.add_task(Task(name, duration=10, priority=priority, due_time=due_time))
print_schedule(Scheduler(owner).generate_schedule(available_minutes=10))
PY
```

Actual CLI output:

```text
Today's Schedule
----------------
08:00  Feeding (10 min) [priority: 3]
```

Feeding (High) is selected ahead of the earlier Play (Low) and Grooming (Medium) tasks. Feeding also wins the time tie-break against Medication, which is High priority and due at 09:00.

## Optional Challenge 4: Professional UI and Output Formatting

The existing interface uses Streamlit's built-in components, and the CLI uses Python string formatting:

| Formatting feature | Implementation | What the owner sees |
|--------------------|----------------|---------------------|
| Structured tables | `st.table()` and `task_row()` in `app.py` | Pet details, current tasks, generated schedules, and skipped tasks. Task rows show time, pet, task, duration, Low/Medium/High priority labels, and To do/Done status. |
| Success messages | `st.success()` | Confirmation when adding a pet or task or saving task edits, plus a schedule summary with task count and minutes used out of the available budget. |
| Conflict warnings | `show_conflicts()` and `st.warning()` | A warning naming the conflicting tasks, pets, date, and time. Both the task list and generated plan show relevant conflicts. |
| Validation and empty states | `st.error()`, `st.warning()`, `st.info()`, and `st.caption()` | Guidance for blank names, duplicate pet names, missing pets/tasks, empty filters, or tasks that do not fit the time budget. |
| Readable CLI output | `print_tasks()`, `print_schedule()`, and `print_warnings()` in `main.py` | Headings and separator lines, due times, durations in minutes, priority values, frequency and status in task listings, and a `WARNING:` prefix for conflicts. |

## 📸 Demo Walkthrough

### Streamlit app

Start the app with `streamlit run app.py` (virtual environment activated) and open the URL it prints.

1. **Add pets.** Leave the owner name as *Jordan*. In the **Pets** form, keep the defaults (*Mochi*, dog, 3) and click **Add pet**. Then enter *Luna*, choose *cat*, and click **Add pet** again. Both pets appear in the pets table. Trying to add a second *Mochi* shows a warning instead of a duplicate.
2. **Create tasks.** In the **Tasks** form, pick a pet and add these tasks one at a time, deliberately out of order:
   - Mochi: *Evening fetch*, 20 min, Low, 18:00
   - Luna: *Give medication*, 5 min, Medium, 09:00
   - Mochi: *Morning walk*, 30 min, High, 08:00
   - Luna: *Feeding*, 10 min, High, 07:30
3. **Sort and filter.** The **Current tasks** table lists them in time order: 07:30 Feeding, 08:00 Morning walk, 09:00 Give medication, 18:00 Evening fetch, each with its pet and a *To do* status. Set **Show pet** to *Mochi* to see only Morning walk and Evening fetch, then set it back to *All pets*.
4. **See a conflict warning.** Add Luna: *Play time*, 15 min, Medium, 08:00. A yellow warning appears under the task list:
   > ⚠️ Task list: Conflict on *(today's date)* at 08:00: Morning walk (Mochi), Play time (Luna). Both tasks are kept; change a time if they can't happen together.
5. **Generate the schedule.** Leave **Available minutes today** at 60 and click **Generate schedule**. The app shows *"Today's Schedule: 4 task(s), 60 of 60 minutes used."* with Feeding, Morning walk, Play time, and Give medication in time order. A *Today's plan* conflict warning repeats the 08:00 clash because both tasks made it into the plan, and *Evening fetch* (Low priority, 20 min) is listed under **Skipped (not enough time left)**.
6. **Edit a task.** In **Edit Task**, select Mochi's *Evening fetch*. Set **New duration (minutes)** to 10 and **New priority** to High, then click **Save changes**. The task table now shows 10 minutes and High priority for the same task. Click **Generate schedule** again: Feeding, Morning walk, Give medication, and Evening fetch appear in time order, using 55 of 60 minutes. Evening fetch is now selected before the Medium-priority tasks; Play time is skipped because it takes 15 minutes and only 10 remain when it is considered. The task-list conflict warning still appears, while the generated plan contains only Morning walk at 08:00.

### CLI demo

`main.py` shows the backend features that the app doesn't expose yet, including recurring tasks. Run it with:

```bash
python main.py
```

Actual output (dates are the day the script runs):

<details>
<summary>Full <code>main.py</code> output</summary>

```text
All tasks (as added)
--------------------
2026-10-18 18:00  Evening fetch (20 min) [priority: 1] [daily] [todo]
2026-10-18 08:00  Morning walk (30 min) [priority: 3] [daily] [todo]
2026-10-18 09:00  Give medication (5 min) [priority: 2] [daily] [todo]
2026-10-18 07:30  Feeding (10 min) [priority: 3] [daily] [todo]
2026-10-18 06:45  Clean litter box (10 min) [priority: 2] [daily] [done]

All tasks (sorted by time)
--------------------------
2026-10-18 06:45  Clean litter box (10 min) [priority: 2] [daily] [done]
2026-10-18 07:30  Feeding (10 min) [priority: 3] [daily] [todo]
2026-10-18 08:00  Morning walk (30 min) [priority: 3] [daily] [todo]
2026-10-18 09:00  Give medication (5 min) [priority: 2] [daily] [todo]
2026-10-18 18:00  Evening fetch (20 min) [priority: 1] [daily] [todo]

Mochi's tasks
-------------
2026-10-18 08:00  Morning walk (30 min) [priority: 3] [daily] [todo]
2026-10-18 18:00  Evening fetch (20 min) [priority: 1] [daily] [todo]

Completed tasks
---------------
2026-10-18 06:45  Clean litter box (10 min) [priority: 2] [daily] [done]

Incomplete tasks
----------------
2026-10-18 07:30  Feeding (10 min) [priority: 3] [daily] [todo]
2026-10-18 08:00  Morning walk (30 min) [priority: 3] [daily] [todo]
2026-10-18 09:00  Give medication (5 min) [priority: 2] [daily] [todo]
2026-10-18 18:00  Evening fetch (20 min) [priority: 1] [daily] [todo]

Today's Schedule
----------------
07:30  Feeding (10 min) [priority: 3]
08:00  Morning walk (30 min) [priority: 3]
09:00  Give medication (5 min) [priority: 2]

=== Recurring tasks ===

Completed daily 'Feeding' (2026-10-18) -> next one due 2026-10-19
Completed it again -> new task: None, Feeding tasks for Luna: 2
Completed weekly 'Bath' (2026-10-18) -> next one due 2026-10-25
Completed one-time 'Vet checkup' -> next one: None

All tasks after completions (sorted by time)
--------------------------------------------
2026-10-18 06:45  Clean litter box (10 min) [priority: 2] [daily] [done]
2026-10-18 07:30  Feeding (10 min) [priority: 3] [daily] [done]
2026-10-18 08:00  Morning walk (30 min) [priority: 3] [daily] [todo]
2026-10-18 09:00  Give medication (5 min) [priority: 2] [daily] [todo]
2026-10-18 11:00  Vet checkup (45 min) [priority: 3] [once] [done]
2026-10-18 16:00  Bath (15 min) [priority: 1] [weekly] [done]
2026-10-18 18:00  Evening fetch (20 min) [priority: 1] [daily] [todo]
2026-10-19 07:30  Feeding (10 min) [priority: 3] [daily] [todo]
2026-10-25 16:00  Bath (15 min) [priority: 1] [weekly] [todo]

Today's Schedule
----------------
08:00  Morning walk (30 min) [priority: 3]
09:00  Give medication (5 min) [priority: 2]
18:00  Evening fetch (20 min) [priority: 1]

=== Conflict detection ===

Conflicts in today's plan:
  No conflicts found.

Conflicts among all incomplete tasks:
  WARNING: Conflict on 2026-10-18 at 08:00: Morning walk (Mochi), Play time (Luna)
  WARNING: Conflict on 2026-10-18 at 18:00: Evening fetch (Mochi), Nail trim (Mochi)
```

</details>
