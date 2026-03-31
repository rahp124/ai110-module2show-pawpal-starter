from pawpal_system import Task, Pet, Owner, Scheduler
from datetime import datetime, timedelta
import pytest

# Test that calling mark_complete() changes the task's status
def test_mark_complete():
    task = Task("Test Task", 30)
    assert not task.is_completed
    task.mark_complete()
    assert task.is_completed

# Test that adding a task to a Pet increases its task count
def test_add_task():
    pet = Pet("Buddy", "Dog", 5)
    assert len(pet.get_tasks()) == 0
    pet.add_task(Task("Test Task", 30))
    assert len(pet.get_tasks()) == 1


# ========================
# 1. SORTING CORRECTNESS
# ========================

def test_sorting_by_priority():
    """
    Verify that Scheduler.sort_by_priority returns tasks sorted by priority (descending),
    then by duration (descending).
    """
    scheduler = Scheduler()
    
    # Create tasks with different priorities and durations
    task_a = Task("Feed dog", time_minutes=30, priority=3)  # Low priority, long
    task_b = Task("Play fetch", time_minutes=20, priority=5)  # High priority, medium
    task_c = Task("Groom", time_minutes=10, priority=5)  # High priority, short
    task_d = Task("Walk dog", time_minutes=45, priority=2)  # Very low priority, very long
    
    tasks = [task_a, task_b, task_c, task_d]
    sorted_tasks = scheduler.sort_by_priority(tasks)
    
    # Expected order: task_b (priority=5, time=20), task_c (priority=5, time=10),
    # task_a (priority=3, time=30), task_d (priority=2, time=45)
    assert sorted_tasks[0] == task_b, "Highest priority task should be first"
    assert sorted_tasks[1] == task_c, "Among same priority, longer duration should come first"
    assert sorted_tasks[2] == task_a, "Lower priority tasks should come after higher priority"
    assert sorted_tasks[3] == task_d, "Lowest priority task should be last"


def test_sorting_empty_list():
    """
    Verify that sorting an empty task list returns an empty list.
    """
    scheduler = Scheduler()
    sorted_tasks = scheduler.sort_by_priority([])
    assert sorted_tasks == []


def test_sorting_single_task():
    """
    Verify that sorting a single task returns that task unchanged.
    """
    scheduler = Scheduler()
    task = Task("Single task", time_minutes=30, priority=3)
    sorted_tasks = scheduler.sort_by_priority([task])
    assert len(sorted_tasks) == 1
    assert sorted_tasks[0] == task


# ========================
# 2. RECURRENCE LOGIC
# ========================

def test_recurring_daily_task_creation():
    """
    Confirm that marking a daily task as complete creates a new task for the following day.
    """
    pet = Pet("Buddy", "Dog", 5)
    task = Task("Feed dog", time_minutes=15, frequency="daily", priority=2)
    pet.add_task(task)
    
    initial_count = len(pet.get_tasks())
    assert initial_count == 1
    
    # Mark the original task as complete
    task.mark_complete(pet=pet)
    
    # Should now have 2 tasks: the completed one and the new recurring one
    assert len(pet.get_tasks()) == 2
    assert task.is_completed
    
    # The new task should be incomplete
    new_task = pet.get_tasks()[1]
    assert not new_task.is_completed
    assert new_task.description == task.description
    assert new_task.frequency == "daily"
    assert new_task.priority == task.priority


def test_recurring_weekly_task_creation():
    """
    Confirm that marking a weekly task as complete creates a new task for the following week.
    """
    pet = Pet("Whiskers", "Cat", 3)
    task = Task("Trim nails", time_minutes=20, frequency="weekly", priority=1)
    pet.add_task(task)
    
    original_task_count = len(pet.get_tasks())
    assert original_task_count == 1
    
    # Mark the weekly task as complete
    task.mark_complete(pet=pet)
    
    # Should now have 2 tasks
    assert len(pet.get_tasks()) == 2
    assert task.is_completed
    
    # Check that the new task was created with future date
    new_task = pet.get_tasks()[1]
    assert not new_task.is_completed
    assert new_task.frequency == "weekly"


def test_recurring_task_without_pet():
    """
    Verify that marking a recurring task complete without a pet does not create a new task.
    """
    task = Task("Feed dog", time_minutes=15, frequency="daily", priority=2)
    
    # Mark complete without providing a pet
    task.mark_complete(pet=None)
    
    # Task should be marked complete but no new task is created
    assert task.is_completed


def test_non_recurring_task():
    """
    Verify that marking a non-recurring task (one-time) as complete does not create a new task.
    """
    pet = Pet("Buddy", "Dog", 5)
    task = Task("Buy new collar", time_minutes=30, frequency="once", priority=3)
    pet.add_task(task)
    
    assert len(pet.get_tasks()) == 1
    
    # Mark as complete with pet provided
    task.mark_complete(pet=pet)
    
    # Should still have only 1 task (no recurring task created)
    assert len(pet.get_tasks()) == 1
    assert task.is_completed


# ========================
# 3. CONFLICT DETECTION
# ========================

def test_detect_conflict_same_scheduled_time(capsys):
    """
    Verify that Scheduler.detect_conflicts prints a warning when two tasks have the same scheduled time.
    """
    scheduler = Scheduler()
    pet = Pet("Buddy", "Dog", 5)
    
    # Add a task with a specific time
    task1 = Task("Morning walk", time_minutes=30, scheduled_time="09:00")
    pet.add_task(task1)
    
    # Create a new task at the same time
    task2 = Task("Morning play", time_minutes=20, scheduled_time="09:00")
    
    # Detect conflict
    conflict_detected = scheduler.detect_conflicts(pet, task2)
    
    # Verify conflict was detected
    assert conflict_detected is True
    
    # Verify warning message was printed
    captured = capsys.readouterr()
    assert "Warning: Task conflict detected" in captured.out
    assert "09:00" in captured.out
    assert "Morning walk" in captured.out
    assert "Morning play" in captured.out


def test_detect_no_conflict_different_times():
    """
    Verify that detect_conflicts returns False when tasks are scheduled at different times.
    """
    scheduler = Scheduler()
    pet = Pet("Buddy", "Dog", 5)
    
    task1 = Task("Morning walk", time_minutes=30, scheduled_time="09:00")
    pet.add_task(task1)
    
    task2 = Task("Evening walk", time_minutes=30, scheduled_time="18:00")
    
    conflict_detected = scheduler.detect_conflicts(pet, task2)
    
    assert conflict_detected is False


def test_detect_conflict_with_no_scheduled_time():
    """
    Verify that detect_conflicts returns False when the new task has no scheduled time.
    """
    scheduler = Scheduler()
    pet = Pet("Buddy", "Dog", 5)
    
    task1 = Task("Morning walk", time_minutes=30, scheduled_time="09:00")
    pet.add_task(task1)
    
    # Task without scheduled time
    task2 = Task("Feed dog", time_minutes=15, scheduled_time=None)
    
    conflict_detected = scheduler.detect_conflicts(pet, task2)
    
    assert conflict_detected is False


def test_add_task_with_conflict_detection(capsys):
    """
    Verify that add_task_with_conflict_detection detects conflicts but still adds the task.
    """
    scheduler = Scheduler()
    pet = Pet("Buddy", "Dog", 5)
    
    task1 = Task("Morning walk", time_minutes=30, scheduled_time="09:00")
    pet.add_task(task1)
    
    task2 = Task("Morning play", time_minutes=20, scheduled_time="09:00")
    
    # Add task with conflict detection
    scheduler.add_task_with_conflict_detection(pet, task2)
    
    # Verify the task was added despite conflict
    assert len(pet.get_tasks()) == 2
    assert task2 in pet.get_tasks()
    
    # Verify warning was printed
    captured = capsys.readouterr()
    assert "Warning: Task conflict detected" in captured.out