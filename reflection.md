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
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

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
