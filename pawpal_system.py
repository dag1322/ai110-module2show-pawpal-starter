from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class Task:
    title: str
    category: str
    duration: int
    priority: str
    due_time: str
    due_date: str
    frequency: str
    notes: str
    completed: bool = False

    def mark_complete(self):
        pass

    def is_due_today(self) -> bool:
        pass

    def create_next_occurrence(self) -> 'Task':
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        pass

    def remove_task(self, task: Task):
        pass

    def get_tasks(self) -> List[Task]:
        pass


class Owner:
    def __init__(self, name: str, available_time: str, preferences: Dict):
        self.name = name
        self.available_time = available_time
        self.preferences = preferences
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        pass

    def get_pet_by_name(self, name: str) -> Optional[Pet]:
        pass

    def get_all_tasks(self) -> List[Task]:
        pass


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def sort_tasks(self, tasks: List[Task]) -> List[Task]:
        pass

    def filter_tasks(self, criteria) -> List[Task]:
        pass

    def detect_conflicts(self, tasks: List[Task]) -> List:
        pass

    def build_daily_plan(self):
        pass

    def explain_choices(self) -> str:
        pass