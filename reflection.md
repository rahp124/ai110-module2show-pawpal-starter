# PawPal+ Project Reflection

## 1. System Design

Core user actions:
Add a pet and basic owner information to the system.
Create and manage care tasks for the pet.
Generate a daily schedule that prioritizes tasks based on priority level and time

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
  Owner: Represents the pet owner. Holds the list of pets and the owner’s available time. Responsible for adding, removing, and listing pets.
  Pet: Represents an individual animal. Holds the list of tasks for that pet. Responsible for adding, removing, and retrieving tasks.
  Task: Represents a single care activity. Contains attributes name, duration, priority, and completion status. Responsible for marking itself complete or incomplete.
  Scheduler – Responsible for generating a daily plan for all pets. Contains methods to collect incomplete tasks, sort them by priority, and generate a schedule that fits within the owner’s available time.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
  Added the collect_pending_tasks method in Scheduler to explicitly gather incomplete tasks from all pets before sorting and planning. Splitting out task collection makes the scheduler logic cleaner, easier to test, and prevents duplication of code inside Pet or Owner.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

**Tradeoff: Exact time match conflict detection vs. overlapping duration checking**

The scheduler detects conflicts by checking if two tasks are scheduled at the **exact same HH:MM time**, rather than checking if their durations overlap. For example, a task at 09:00 lasting 30 minutes will conflict with a task at 09:00 lasting 15 minutes, but NOT with a task at 09:15 lasting 20 minutes (even though they may overlap by 15 minutes).

**Why this tradeoff is reasonable:**

- **Simplicity**: This approach is lightweight and O(n) in complexity, making it fast for real-world pet care scenarios with a typical number of tasks.
- **User intent**: In pet care, owners often schedule tasks in "slots" (e.g., "morning feeding time", "evening walk"). Checking exact time matches aligns with this mental model rather than precise duration overlap.
- **MVP approach**: For an initial version, exact matching is sufficient. The system warns users about conflicts and allows them to add tasks anyway, giving owners flexibility while still providing alerts.
- **Scalability path**: If needed, we can evolve to duration-based overlap detection later without major refactoring—the conflict detection interface stays the same.

This tradeoff prioritizes usability and implementation speed over precision, which is appropriate for a pet care system where tasks are typically discrete, non-overlapping activities.

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
