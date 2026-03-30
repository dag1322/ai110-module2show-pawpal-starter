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

My scheduler considers three main constraints: due time and due date, priority levels (high/medium/low), and task frequency. I decided priority mattered most because pet owners need critical care (feeding, medication) to happen before optional tasks, so the sort_tasks method prioritizes by urgency first. Due date comes second because tasks on the same priority level should be ordered by when they're due. Time-based sorting is available as an alternative view when owners want to see their schedule chronologically instead. Owner available_time was flagged as a constraint but kept simple in this MVP since most pet owners have flexible hours for care tasks. Overall, I weighted the scheduler to focus on getting important tasks scheduled first, then ordering by deadline, trusting the owner to handle time availability manually.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff my scheduler makes is only checking for exact time matches (same due_time and due_date) instead of considering task durations for overlapping schedules. This means if two tasks are at 14:00 but one takes 10 minutes and the other 30 minutes, it won't detect a potential overlap at 14:10. This tradeoff is reasonable for this scenario because pet care tasks are often short and discrete, and adding duration-based logic would complicate the code without much benefit for a simple app. It keeps the system lightweight and focused on basic conflicts.

---

## 3. AI Collaboration

**a. How you used AI**

- I used VS Code Copilot as an interactive coding partner for each phase: UML translation, class skeleton creation, logic implementation, and Streamlit integration.
- Prompts like "add conflict detection", "sort by HH:MM", "filter tasks by pet" produced actionable code snippets with minimal cognitive load.

**b. Which Copilot features were most effective?**

- Inline suggestions in the editor was very extremely helpful for method body logic (e.g., `sort_by_time` and `filter_tasks`).
- Chat completions gave structured implementation templates and test ideas.
- Auto-complete with type hints ensured method signatures matched your design.

**c. One suggestion I rejected or modified**

- Copilot initially suggested doing all scheduling logic inside the Owner class. I rejected that and instead kept Scheduler as the dedicated planning component to preserve single-responsibility design.
- I also fixed conflict detection logic from the complex interval overlap approach to an specific time warning approach to avoid unnecessary complexity.

**d. Separate chat sessions for phases**

- Separating phases into distinct sessions kept goals focused: phase 1 for UML, phase 2 for core class logic, phase 3 for UI integration and tests.
- This segmentation avoided context drift and made it easy to review and validate each step independently.

**e. Lead architect reflection**

- Acting as the architect meant evaluating AI suggestions, choosing the clean design, and taking responsibility for final behavior.
- I learned that the AI provides great code scaffolding, but the human must define constraints, test paths, and tradeoffs.
- The biggest value is combining AI speed with human judgment to form a robust system.

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
