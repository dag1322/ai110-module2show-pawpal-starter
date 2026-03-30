from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta


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
        self.completed = True

    def is_due_today(self) -> bool:
        today = datetime.now().date()
        due = datetime.strptime(self.due_date, "%Y-%m-%d").date()
        return due == today

    def create_next_occurrence(self) -> 'Task':
        due = datetime.strptime(self.due_date, "%Y-%m-%d").date()
        if self.frequency == "daily":
            new_due = due + timedelta(days=1)
        elif self.frequency == "weekly":
            new_due = due + timedelta(weeks=1)
        elif self.frequency == "monthly":
            # Approximate monthly
            new_month = due.month % 12 + 1
            new_year = due.year + (due.month // 12)
            try:
                new_due = due.replace(month=new_month, year=new_year)
            except ValueError:  # e.g., Feb 30
                new_due = due.replace(month=new_month, year=new_year, day=28)
        else:
            new_due = due  # No recurrence
        return Task(
            title=self.title,
            category=self.category,
            duration=self.duration,
            priority=self.priority,
            due_time=self.due_time,
            due_date=new_due.strftime("%Y-%m-%d"),
            frequency=self.frequency,
            notes=self.notes,
            completed=False
        )


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        self.tasks.append(task)

    def remove_task(self, task: Task):
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self) -> List[Task]:
        return self.tasks


class Owner:
    def __init__(self, name: str, available_time: str, preferences: Dict):
        self.name = name
        self.available_time = available_time
        self.preferences = preferences
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        self.pets.append(pet)

    def get_pet_by_name(self, name: str) -> Optional[Pet]:
        for pet in self.pets:
            if pet.name == name:
                return pet
        return None

    def get_all_tasks(self) -> List[Task]:
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def sort_tasks(self, tasks: List[Task]) -> List[Task]:
        # Sort by priority (high, medium, low), then by due_date
        priority_order = {"high": 0, "medium": 1, "low": 2}
        return sorted(tasks, key=lambda t: (priority_order.get(t.priority, 3), t.due_date))

    def filter_tasks(self, criteria: Dict[str, Any]) -> List[Task]:
        # Filter tasks based on criteria dict, e.g., {"category": "feeding", "completed": False}
        all_tasks = self.owner.get_all_tasks()
        filtered = []
        for task in all_tasks:
            match = True
            for key, value in criteria.items():
                if getattr(task, key, None) != value:
                    match = False
                    break
            if match:
                filtered.append(task)
        return filtered

    def detect_conflicts(self, tasks: List[Task]) -> List[Dict[str, str]]:
        # Detect conflicts: tasks with same due_time and due_date
        conflicts = []
        for i, task1 in enumerate(tasks):
            for j, task2 in enumerate(tasks):
                if i < j and task1.due_time == task2.due_time and task1.due_date == task2.due_date:
                    conflicts.append({
                        "task1": task1.title,
                        "task2": task2.title,
                        "reason": f"Both scheduled at {task1.due_time} on {task1.due_date}"
                    })
        return conflicts

    def build_daily_plan(self) -> List[Task]:
        # Build plan for today: get due tasks, sort them
        all_tasks = self.owner.get_all_tasks()
        today_tasks = [t for t in all_tasks if t.is_due_today() and not t.completed]
        return self.sort_tasks(today_tasks)

    def explain_choices(self) -> str:
        plan = self.build_daily_plan()
        if not plan:
            return "No tasks due today."
        explanation = "Daily plan sorted by priority and due date:\n"
        for task in plan:
            explanation += f"- {task.title} ({task.priority} priority, {task.due_time})\n"
        return explanation