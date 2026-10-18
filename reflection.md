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

- Why is that tradeoff reasonable for this scenario?

I think this is reasonable because essential care tasks should come before optional activities. The scheduler also tries to use the remaining time by checking whether shorter tasks can still fit.

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
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
