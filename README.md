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

## Smarter Scheduling

This implementation includes advanced scheduling features:

### Recurring Tasks

Tasks with `frequency="daily"` or `frequency="weekly"` automatically create new instances when marked complete. Daily tasks are scheduled for the next day, and weekly tasks for seven days ahead. This eliminates manual re-adding of routine pet care activities.

### Conflict Detection

The scheduler detects when two tasks are scheduled at the same time (HH:MM format) and prints a warning, alerting the owner to potential scheduling conflicts. Tasks can still be added despite conflicts, giving users full control while providing helpful guidance.

### Priority-Based Planning

The `generate_daily_plan()` method builds an optimal schedule by sorting tasks by priority (highest first) and duration, then fitting as many tasks as possible within the owner's available time. This ensures critical care tasks always get scheduled first.

### Task Filtering

Multiple filtering options allow owners to view tasks by completion status, specific pet, or priority level, making it easy to focus on what matters most.

## Testing PawPal+

### Run Tests

```bash
python -m pytest tests/test_pawpal.py -v
```

### Test Coverage

The test suite includes **13 comprehensive tests** covering three critical areas:

1. **Sorting Correctness** (3 tests)
   - Verifies tasks sort by priority (highest first), then by duration (longest first)
   - Tests edge cases: empty task lists and single-task lists

2. **Recurrence Logic** (4 tests)
   - Confirms daily tasks generate next-day occurrences when marked complete
   - Confirms weekly tasks generate next-week occurrences
   - Verifies that one-time tasks don't create recurring instances
   - Tests that recurring tasks require a pet object to be created

3. **Conflict Detection** (4 tests)
   - Verifies warnings print when two tasks share the same scheduled time
   - Tests that tasks at different times don't trigger conflicts
   - Tests that unscheduled tasks don't cause false positives
   - Confirms tasks are added despite conflicts (user control preserved)

4. **Existing Tests** (2 tests)
   - Task completion status tracking
   - Pet task management

### Confidence Level

⭐⭐⭐⭐ (4/5 stars)

**Why 4 stars:**
- ✅ All 13 tests pass consistently
- ✅ Core scheduling, sorting, and recurrence logic thoroughly validated
- ✅ Edge cases handled (empty lists, None values, conflicts)
- ⚠️ Integration with Streamlit UI not yet tested
- ⚠️ No stress tests for large task volumes
- ⚠️ Date/time boundary cases (year wrap-around, DST) not covered

The system is production-ready for typical use cases, but would benefit from UI testing and performance validation before wide deployment.
