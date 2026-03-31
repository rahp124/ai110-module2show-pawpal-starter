from pawpal_system import Task, Pet, Owner, Scheduler

owner = Owner("Alice")
dog = Pet("Buddy", "Dog", 5)
cat = Pet("Mittens", "Cat", 3)
owner.add_pet(dog)
owner.add_pet(cat)

dog.add_task(Task("Walk Buddy", 30, priority=5))
dog.add_task(Task("Feed Buddy", 10, priority=3))
cat.add_task(Task("Feed Mittens", 10, priority=4))

scheduler = Scheduler()
plan = scheduler.generate_daily_plan(owner, available_time=40)

print("Today's Schedule:")
for i, task in enumerate(plan, start=1):
    print(f"{i}. {task.description} ({task.time_minutes} min, priority {task.priority})")