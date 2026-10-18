# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

The three main actions I want users to perform are adding their pets, creating care tasks for each pet, and generating a daily schedule based on task priorities and available time.

- Briefly describe your initial UML design.

My initial design has four classes: Owner, Pet, Task, and Scheduler.
An owner can have multiple pets, and each pet can have multiple
care tasks. The scheduler organizes those tasks into a daily schedule.

- What classes did you include, and what responsibilities did you assign to each?

I included Owner to manage pets, Pet to store information about
each pet and its tasks, Task to represent activities like feeding
or walking, and Scheduler to organize tasks based on their
priority and time.

**b. Design changes**

- Did your design change during implementation?

Yes, I made a few changes after reviewing my initial design with AI.

- If yes, describe at least one change and why you made it.

Originally, the Scheduler had its own list of tasks, separate
from the tasks stored in each Pet. I changed it so the Scheduler
gets tasks through the Owner instead. This avoids having two
separate lists that could become inconsistent.

I also changed priority from a string to an integer and added
an available_minutes parameter so the scheduler can eventually
organize tasks based on priority and available time.

---
    
## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

My scheduler considers task priority, duration, due time, and the total time available. It prioritizes higher-priority tasks and uses due time to break ties. It also skips completed tasks and tasks that don’t fit within the available time.

- How did you decide which constraints mattered most?

I focused on priority and available time because some pet care tasks are more important than others, and owners might not have enough time to complete everything. Due time helps organize the selected tasks into a daily schedule.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

My scheduler prioritizes more important tasks over less important ones, even if that means skipping some activities. For example, it might choose feeding and medication over playtime when there isn’t enough time for everything.

Another tradeoff is that conflict detection only flags tasks with exactly the same date and time. It doesn't check whether task durations overlap, so a 30-minute walk at 08:00 and a feeding at 08:15 would not be flagged.

- Why is that tradeoff reasonable for this scenario?

I think this is reasonable because essential care tasks should come before optional activities. The scheduler also tries to use the remaining time by checking whether shorter tasks can still fit.

For conflicts, exact matching keeps the logic simple and easy to test. Most pet care tasks are short and usually set at round times, so it still catches the most common mistake of booking two things at the same time. Since the scheduler only shows a warning and doesn't remove anything, the owner can still decide what to do. I also chose to keep the explicit loops in detect_conflicts() instead of a shorter, more "Pythonic" version because they are easier to follow, and performance isn't an issue with only a handful of tasks per day. Checking overlapping durations would be a good next improvement.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

I used Claude to help design the UML diagram, generate the initial Python class skeletons, and implement the core functionality. I also used it to review the architecture, identify potential problems, and write tests.

- What kinds of prompts or questions were most helpful?

The most helpful prompts were asking Claude to review my existing code and identify problems before making changes. This helped me catch an issue where the Scheduler and Pet classes stored separate task lists.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

Claude suggested several improvements, including changing how the Scheduler accesses tasks and adding more input validation. I decided to focus on fixing the relationship between Scheduler and Owner rather than implementing every suggested feature immediately.

- How did you evaluate or verify what the AI suggested?

I reviewed the updated UML diagram using Mermaid Live Editor, ran the demo script to check the scheduling output, and used pytest to verify task completion and task addition. Both tests passed.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

The initial backend suite contained 10 pytest tests in `tests/test_pawpal.py`. They check that a task can be marked complete and added to a pet, that `sort_by_time()` orders tasks by time and puts earlier dates first without changing the original list, that completing a daily task creates a new task for tomorrow and a weekly task creates one 7 days later, and that completing the same task twice doesn't create a duplicate. They also check that two tasks with the same date and time are flagged as a conflict, that the same time on different dates is not, and that a pet with no tasks doesn't cause errors when filtering, scheduling, or checking for conflicts.

- Why were these tests important?

These are the parts of the scheduler that are easiest to get wrong. Recurrence depends on date calculations and could easily create duplicate tasks, and conflict detection needs to catch real clashes without giving false warnings. The tests calculate dates from `date.today()` instead of using fixed dates, so they keep passing on any day. Along with the tests, I ran `main.py` after each change to check the output.

**b. Confidence**

- How confident are you that your scheduler works correctly?

I would rate my confidence 4 out of 5. All 10 tests pass, including sorting, recurrence, and conflict detection. However, some scheduling behaviors, like choosing tasks by priority under the time limit and leaving out completed or future tasks, don't have their own tests yet, and the Streamlit UI isn't covered by automated tests.

- What edge cases would you test next if you had more time?

I would add tests for `generate_schedule()` choosing tasks by priority and skipping tasks that don't fit, leaving out completed and future-dated tasks, one-time tasks not repeating, completing a task that doesn't belong to any pet, and two tasks for the same pet at the same time. I would also test inputs the code doesn't validate yet, like times that aren't zero-padded ("9:00"), a frequency with extra spaces ("daily "), and negative available minutes.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I'm most satisfied that the project became a working application with a modular backend and a Streamlit interface. The logic lives in `pawpal_system.py`, separate from the UI, so the same classes are used by `main.py`, the tests, and `app.py`. Keeping tasks in one place, on each pet, with the Scheduler reading them through the Owner, made it easier to add sorting, filtering, recurrence, and conflict detection later without changing the overall design.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would add a way to mark tasks complete in the Streamlit app, so recurring tasks would also show up in the UI instead of only in the CLI demo. I would also add persistence so pets and tasks aren't lost when the page is refreshed, and improve conflict detection to catch overlapping durations instead of only exact time matches.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

AI can speed up development a lot. Claude helped me with the design, implementation, and testing throughout this project. But reviewing and verifying the generated code is still important. Asking for a review before making changes, deciding which suggestions to accept, and running the tests and demo after each step helped me make sure the code did what I expected and that the design stayed simple.
