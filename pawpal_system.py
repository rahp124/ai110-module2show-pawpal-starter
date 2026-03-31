from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
	name: str
	duration: int
	priority: int
	is_completed: bool = False

	def mark_complete(self) -> None:
		pass

	def mark_incomplete(self) -> None:
		pass


@dataclass
class Pet:
	name: str
	species: str
	age: int
	tasks: List[Task] = field(default_factory=list)

	def add_task(self, task: Task) -> None:
		pass

	def remove_task(self, task_name: str) -> None:
		pass

	def get_tasks(self) -> List[Task]:
		pass


class Owner:
	def __init__(self, name: str) -> None:
		self.name = name
		self.pets: List[Pet] = []

	def add_pet(self, pet: Pet) -> None:
		pass

	def remove_pet(self, pet_name: str) -> None:
		pass

	def get_pets(self) -> List[Pet]:
		pass


class Scheduler:
	def generate_daily_plan(self, owner: Owner, available_time: int) -> List[Task]:
		pass

	def collect_pending_tasks(self, owner: Owner) -> List[Task]:
		pass

	def sort_by_priority(self, tasks: List[Task]) -> List[Task]:
		pass
