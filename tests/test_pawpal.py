from pawpal_system import Task, Pet

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