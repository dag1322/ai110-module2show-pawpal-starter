from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from itertools import combinations


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
        """Mark the task as completed."""
        self.completed = True

    def is_due_today(self) -> bool:
        """Check if the task is due today."""
        today = datetime.now().date()
        due = datetime.strptime(self.due_date, "%Y-%m-%d").date()
        return due == today

    def create_next_occurrence(self) -> 'Task':
        """Create the next occurrence of a recurring task."""
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
        """Add a task to the pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task):
        """Remove a task from the pet's task list."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self) -> List[Task]:
        """Get all tasks for the pet."""
        return self.tasks


class Owner:
    def __init__(self, name: str, available_time: str, preferences: Dict):
        """Initialize the owner with name, available time, and preferences."""
        self.name = name
        self.available_time = available_time
        self.preferences = preferences
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        """Add a pet to the owner's pet list."""
        self.pets.append(pet)

    def get_pet_by_name(self, name: str) -> Optional[Pet]:
        """Get a pet by name."""
        for pet in self.pets:
            if pet.name == name:
                return pet
        return None

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks from all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    def __init__(self, owner: Owner):
        """Initialize the scheduler with an owner."""
        self.owner = owner

    def sort_tasks(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by priority and due date."""
        # Sort by priority (high, medium, low), then by due_date
        priority_order = {"high": 0, "medium": 1, "low": 2}
        return sorted(tasks, key=lambda t: (priority_order.get(t.priority, 3), t.due_date))

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by due_time in HH:MM format."""
        return sorted(tasks, key=lambda t: datetime.strptime(t.due_time, "%H:%M").time())

    def filter_tasks_by_status(self, completed: bool) -> List[Task]:
        """Filter tasks by completion status."""
        all_tasks = self.owner.get_all_tasks()
        return [t for t in all_tasks if t.completed == completed]

    def filter_tasks_for_pet(self, pet_name: str) -> List[Task]:
        """Filter tasks for a specific pet."""
        pet = self.owner.get_pet_by_name(pet_name)
        return pet.get_tasks() if pet else []

    def filter_tasks(self, criteria: Dict[str, Any]) -> List[Task]:
        """Filter tasks based on criteria."""
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

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """Detect scheduling conflicts and return warning messages."""
        warnings = []
        # Check for same time across all tasks
        for task1, task2 in combinations(tasks, 2):
            if task1.due_time == task2.due_time and task1.due_date == task2.due_date:
                warnings.append(f"Conflict: '{task1.title}' and '{task2.title}' are both scheduled at {task1.due_time} on {task1.due_date}.")
        # Check for same pet conflicts
        for pet in self.owner.pets:
            pet_tasks = pet.get_tasks()
            for task1, task2 in combinations(pet_tasks, 2):
                if task1.due_time == task2.due_time and task1.due_date == task2.due_date:
                    warnings.append(f"Pet conflict for {pet.name}: '{task1.title}' and '{task2.title}' overlap at {task1.due_time} on {task1.due_date}.")
        return warnings

    def build_daily_plan(self) -> List[Task]:
        """Build the daily plan of tasks due today."""
        # Build plan for today: get due tasks, sort them
        all_tasks = self.owner.get_all_tasks()
        today_tasks = [t for t in all_tasks if t.is_due_today() and not t.completed]
        return self.sort_tasks(today_tasks)

    def mark_task_complete(self, task: Task, pet_name: str):
        """Mark a task complete and handle recurring tasks."""
        task.mark_complete()
        if task.frequency in ["daily", "weekly"]:
            pet = self.owner.get_pet_by_name(pet_name)
            if pet:
                next_task = task.create_next_occurrence()
                pet.add_task(next_task)

    def explain_choices(self) -> str:
        """Explain the choices made in the daily plan."""
        plan = self.build_daily_plan()
        if not plan:
            return "No tasks due today."
        explanation = "Daily plan sorted by priority and due date:\n"
        for task in plan:
            explanation += f"- {task.title} ({task.priority} priority, {task.due_time})\n"
        return explanation