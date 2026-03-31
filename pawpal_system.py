from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
	description: str
	time_minutes: int
	frequency: str = "daily"
	priority: int = 1
	is_completed: bool = False

	def mark_complete(self) -> None:
		"""
		Mark the task or item as completed.
		
		Sets the is_completed attribute to True, indicating that this task or item
		has been finished.
		"""
		self.is_completed = True

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
		for i, task in enumerate(self.tasks):
			if task.description == task_description:
				del self.tasks[i]
				return True
		return False

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
		for i, pet in enumerate(self.pets):
			if pet.name == pet_name:
				del self.pets[i]
				return True
		return False

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
		all_tasks: List[Task] = []
		for pet in self.pets:
			if include_completed:
				all_tasks.extend(pet.get_tasks())
			else:
				all_tasks.extend(pet.get_pending_tasks())
		return all_tasks


class Scheduler:
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

		pending_tasks = self.collect_pending_tasks(owner)
		sorted_tasks = self.sort_by_priority(pending_tasks)

		plan: List[Task] = []
		time_used = 0

		for task in sorted_tasks:
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
		Sorts a list of tasks by priority and duration in descending order.
		
		Tasks are sorted first by priority (highest first), and then by time in minutes
		(longest first) for tasks with the same priority.
		
		Args:
			tasks (List[Task]): A list of Task objects to be sorted.
		
		Returns:
			List[Task]: A new list of tasks sorted by priority (descending) and time in minutes (descending).
		
		Example:
			>>> tasks = [Task("A", 1, 30), Task("B", 2, 45), Task("C", 1, 20)]
			>>> sorted_tasks = sort_by_priority(tasks)
			>>> # Returns tasks sorted by highest priority first, then longest duration
		"""
		return sorted(tasks, key=lambda task: (task.priority, -task.time_minutes), reverse=True)
