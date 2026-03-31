from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List


@dataclass
class Task:
	description: str
	time_minutes: int
	frequency: str = "daily"
	priority: int = 1
	is_completed: bool = False
	scheduled_date: datetime | None = None
	scheduled_time: str | None = None  # Time in HH:MM format (e.g., "09:00")

	def mark_complete(self, pet: Pet | None = None) -> None:
		"""
		Mark the task as completed and create a recurring task if applicable.
		
		Sets the is_completed attribute to True. If the task has a recurring frequency
		("daily" or "weekly") and a pet is provided, a new task is automatically created
		for the next occurrence and added to the pet's task list.
		
		Args:
			pet (Pet | None): The pet object to add the recurring task to. If provided and
				the task has a recurring frequency, a new task will be created.
		"""
		self.is_completed = True
		
		# Create recurring task if applicable
		recurrence_days = {"daily": 1, "weekly": 7}
		if pet is not None and self.frequency in recurrence_days:
			next_date = datetime.now() + timedelta(days=recurrence_days[self.frequency])
			
			new_task = Task(
				description=self.description,
				time_minutes=self.time_minutes,
				frequency=self.frequency,
				priority=self.priority,
				is_completed=False,
				scheduled_date=next_date
			)
			pet.add_task(new_task)

	def mark_incomplete(self) -> None:
		"""
		Mark the task as incomplete.
		
		Sets the is_completed attribute to False, indicating that the task
		has not been completed or needs to be redone.
		"""
		self.is_completed = False


@dataclass
class Pet:
	name: str
	species: str
	age: int
	tasks: List[Task] = field(default_factory=list)

	def add_task(self, task: Task) -> None:
		"""
		Add a new task to the task list.
		
		Args:
			task (Task): The task object to be added to the collection.
		
		Returns:
			None
		"""
		self.tasks.append(task)

	def remove_task(self, task_description: str) -> bool:
		"""
		Removes a task from the task list based on its description.

		Args:
			task_description (str): The description of the task to remove.

		Returns:
			bool: True if the task was found and removed, False otherwise.
		"""
		initial_length = len(self.tasks)
		self.tasks = [task for task in self.tasks if task.description != task_description]
		return len(self.tasks) < initial_length

	def get_tasks(self) -> List[Task]:
		"""
		Returns a list of all tasks.

		Returns:
			List[Task]: A list containing all Task objects managed by this instance.
		"""
		return list(self.tasks)

	def get_pending_tasks(self) -> List[Task]:
		"""
		Retrieve all pending tasks that have not been completed.
		
		Returns:
			List[Task]: A list of Task objects where is_completed is False.
		"""
		return [task for task in self.tasks if not task.is_completed]


class Owner:
	def __init__(self, name: str) -> None:
		"""
		Initialize a PawPal system instance.
		
		Args:
			name (str): The name of the PawPal system.
		
		Attributes:
			name (str): The name of the PawPal system.
			pets (List[Pet]): A list to store Pet objects managed by the system.
		"""
		self.name = name
		self.pets: List[Pet] = []

	def add_pet(self, pet: Pet) -> None:
		"""
		Add a pet to the system.
		
		Args:
			pet (Pet): The pet object to be added to the pets list.
		
		Returns:
			None
		"""
		self.pets.append(pet)

	def remove_pet(self, pet_name: str) -> bool:
		"""
		Removes a pet from the pets list by its name.

		Args:
			pet_name (str): The name of the pet to remove.

		Returns:
			bool: True if the pet was found and removed, False otherwise.
		"""
		initial_length = len(self.pets)
		self.pets = [pet for pet in self.pets if pet.name != pet_name]
		return len(self.pets) < initial_length

	def get_pets(self) -> List[Pet]:
		"""
		Returns a list of all pets in the system.

		Returns:
			List[Pet]: A list containing all Pet objects managed by the system.
		"""
		return list(self.pets)

	def get_all_tasks(self, include_completed: bool = True) -> List[Task]:
		"""
		Retrieve all tasks associated with the pets in the system.

		Args:
			include_completed (bool, optional): If True, include both completed and pending tasks.
				If False, include only pending tasks. Defaults to True.

		Returns:
			List[Task]: A list of Task objects collected from all pets, filtered based on the
				completion status as specified by the include_completed parameter.
		"""
		task_getter = (lambda pet: pet.get_tasks()) if include_completed else (lambda pet: pet.get_pending_tasks())
		return [task for pet in self.pets for task in task_getter(pet)]


class Scheduler:
	def detect_conflicts(self, pet: Pet, new_task: Task) -> bool:
		"""
		Detect if a new task conflicts with existing tasks based on scheduled time.
		
		Checks if the new task is scheduled at the same time (HH:MM) as any existing
		task for the pet. If a conflict is found, prints a warning message.
		
		Args:
			pet (Pet): The pet whose tasks to check for conflicts.
			new_task (Task): The task to check for conflicts.
		
		Returns:
			bool: True if a conflict is detected, False otherwise.
		"""
		if new_task.scheduled_time is None:
			return False
		
		conflicting_task = next(
			(task for task in pet.get_tasks() if task.scheduled_time == new_task.scheduled_time),
			None
		)
		
		if conflicting_task:
			print(f"Warning: Task conflict detected at {new_task.scheduled_time} "
				f"between {conflicting_task.description} and {new_task.description}")
		return conflicting_task is not None
	
	def add_task_with_conflict_detection(self, pet: Pet, new_task: Task) -> None:
		"""
		Add a task to a pet with conflict detection.
		
		Detects and prints warnings for any time conflicts, but adds the task regardless.
		
		Args:
			pet (Pet): The pet to add the task to.
			new_task (Task): The task to add.
		
		Returns:
			None
		"""
		self.detect_conflicts(pet, new_task)
		pet.add_task(new_task)

	def filter_tasks_by_completion(self, owner: Owner, is_completed: bool) -> List[Task]:
		"""
			Filter all tasks for the owner's pets by completion status.
			Args:
				owner (Owner): The owner whose pets' tasks to filter.
				is_completed (bool): True to get completed tasks, False for incomplete tasks.
			Returns:
				List[Task]: List of tasks matching the completion status.
		"""
		all_tasks = owner.get_all_tasks(include_completed=True)
		return [task for task in all_tasks if task.is_completed == is_completed]

	def filter_tasks_by_pet_name(self, owner: Owner, pet_name: str) -> List[Task]:
		"""
			Filter all tasks for a specific pet by name.
			Args:
				owner (Owner): The owner whose pets' tasks to filter.
				pet_name (str): The name of the pet whose tasks to retrieve.
			Returns:
				List[Task]: List of tasks for the specified pet, or empty if not found.
		"""
		pet = next((pet for pet in owner.get_pets() if pet.name == pet_name), None)
		return pet.get_tasks() if pet else []
	def generate_daily_plan(self, owner: Owner, available_time: int) -> List[Task]:
		"""
		Generates a daily plan of tasks for the given owner based on available time.

		This method collects all pending tasks for the owner, sorts them by priority,
		and selects as many tasks as possible without exceeding the specified available time.

		Args:
			owner (Owner): The owner for whom to generate the daily plan.
			available_time (int): The total available time in minutes for the day.

		Returns:
			List[Task]: A list of tasks scheduled for the day, prioritized and fitting within the available time.
		"""
		if available_time <= 0:
			return []

		plan = []
		time_used = 0
		
		for task in self.sort_by_priority(self.collect_pending_tasks(owner)):
			if time_used + task.time_minutes <= available_time:
				plan.append(task)
				time_used += task.time_minutes
		
		return plan

	def collect_pending_tasks(self, owner: Owner) -> List[Task]:
		"""
		Retrieve all pending (incomplete) tasks for a given owner.
		
		Args:
			owner (Owner): The owner object whose pending tasks should be retrieved.
		
		Returns:
			List[Task]: A list of Task objects that are not yet completed for the specified owner.
		"""
		return owner.get_all_tasks(include_completed=False)

	def sort_by_priority(self, tasks: List[Task]) -> List[Task]:
		"""
		Sort tasks by priority and duration in descending order.
		
		Tasks are sorted first by priority (highest first), and secondarily by time duration
		(longest first) to handle ties. This ensures that high-priority tasks are scheduled first,
		and among equal-priority tasks, longer tasks are prioritized to fit better in available time.
		
		Args:
			tasks (List[Task]): The list of tasks to sort.
		
		Returns:
			List[Task]: A new sorted list of tasks ordered by priority (descending) then duration (descending).
		
		Example:
			Task A: priority=3, time=30 min
			Task B: priority=5, time=20 min
			Task C: priority=5, time=10 min
			
			Result: [Task B, Task C, Task A] (sorted by -priority, then -time_minutes)
		"""
		return sorted(tasks, key=lambda task: (-task.priority, -task.time_minutes))
