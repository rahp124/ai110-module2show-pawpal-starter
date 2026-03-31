from pawpal_system import Task, Pet, Owner, Scheduler

owner = Owner("Alice")
dog = Pet("Buddy", "Dog", 5)
cat = Pet("Mittens", "Cat", 3)
owner.add_pet(dog)
owner.add_pet(cat)

print("=" * 60)
print("CONFLICT DETECTION TEST")
print("=" * 60)

# Test conflict detection with Buddy
print(f"\nAdding tasks to {dog.name}:")
scheduler = Scheduler()

# Add first task at 09:00
task1 = Task("Feed Buddy", 10, priority=3, scheduled_time="09:00")
scheduler.add_task_with_conflict_detection(dog, task1)
print(f"✓ Added: {task1.description} at {task1.scheduled_time}")

# Add second task at same time - should trigger conflict warning
task2 = Task("Walk Buddy", 30, priority=5, scheduled_time="09:00")
scheduler.add_task_with_conflict_detection(dog, task2)
print(f"✓ Added: {task2.description} at {task2.scheduled_time}")

# Add task at different time - no conflict
task3 = Task("Brush Buddy", 5, priority=1, scheduled_time="10:30")
scheduler.add_task_with_conflict_detection(dog, task3)
print(f"✓ Added: {task3.description} at {task3.scheduled_time}")

print(f"\nAdding tasks to {cat.name}:")

# Add tasks to cat
task4 = Task("Feed Mittens", 10, priority=4, scheduled_time="08:00")
scheduler.add_task_with_conflict_detection(cat, task4)
print(f"✓ Added: {task4.description} at {task4.scheduled_time}")

task5 = Task("Play with Mittens", 15, priority=2, scheduled_time="14:00")
scheduler.add_task_with_conflict_detection(cat, task5)
print(f"✓ Added: {task5.description} at {task5.scheduled_time}")

print("\n" + "=" * 60)
print("ALL TASKS VERIFICATION")
print("=" * 60)

# Print all tasks for each pet with their scheduled times
print(f"\n{dog.name}'s Tasks:")
for i, task in enumerate(dog.get_tasks(), start=1):
    time_info = f" at {task.scheduled_time}" if task.scheduled_time else ""
    print(f"  {i}. {task.description} ({task.time_minutes} min, priority {task.priority}){time_info}")

print(f"\n{cat.name}'s Tasks:")
for i, task in enumerate(cat.get_tasks(), start=1):
    time_info = f" at {task.scheduled_time}" if task.scheduled_time else ""
    print(f"  {i}. {task.description} ({task.time_minutes} min, priority {task.priority}){time_info}")

# Verify task counts
print(f"\nTask Summary:")
print(f"  {dog.name}: {len(dog.get_tasks())} tasks")
print(f"  {cat.name}: {len(cat.get_tasks())} tasks")
print(f"  Total: {len(owner.get_all_tasks())} tasks")

scheduler = Scheduler()