# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML design had four main classes: Owner, Pet, Task, and Scheduler. The Task class represented things like walks, feeding, or meds, and stored info like how long it takes, priority, due time, and whether it’s done. The Pet class represented each pet and kept track of all their tasks. The Owner class represented the user and stored all the pets, plus things like how much time they have in a day. The Scheduler class was basically the “brain” of the app, since it collected all the tasks, sorted them, checked for conflicts, and built a daily plan based on priority and time. Overall, I tried to keep things organized by separating the data (Owner, Pet, Task) from the logic (Scheduler).

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, my design did change while I was building it. At first, I thought about putting all the scheduling logic inside the Owner class, but it got messy really fast and made the class do too much. So I decided to create a separate Scheduler class just for handling the planning part. This made things a lot cleaner because now the Owner just stores pets and info, and the Scheduler handles things like sorting tasks, checking conflicts, and building the plan. This change made the code easier to understand and follow.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff my scheduler makes is only checking for exact time matches (same due_time and due_date) instead of considering task durations for overlapping schedules. This means if two tasks are at 14:00 but one takes 10 minutes and the other 30 minutes, it won't detect a potential overlap at 14:10. This tradeoff is reasonable for this scenario because pet care tasks are often short and discrete, and adding duration-based logic would complicate the code without much benefit for a simple app. It keeps the system lightweight and focused on basic conflicts.

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
