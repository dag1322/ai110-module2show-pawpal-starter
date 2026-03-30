from pawpal_system import Owner, Pet, Task, Scheduler

# Create an Owner
owner = Owner("John Doe", "9am-5pm", {"theme": "dark"})

# Create Pets
pet1 = Pet("Fluffy", "Cat", 3)
pet2 = Pet("Buddy", "Dog", 5)

# Add pets to owner
owner.add_pet(pet1)
owner.add_pet(pet2)

# Create Tasks with different times
task1 = Task("Feed Fluffy", "feeding", 10, "high", "08:00", "2026-03-30", "daily", "Morning feed")
task2 = Task("Walk Buddy", "exercise", 30, "medium", "10:00", "2026-03-30", "daily", "Daily walk")
task3 = Task("Groom Fluffy", "grooming", 20, "low", "14:00", "2026-03-30", "weekly", "Brush fur")

# Add tasks to pets
pet1.add_task(task1)
pet1.add_task(task3)
pet2.add_task(task2)

# Create Scheduler
scheduler = Scheduler(owner)

# Print Today's Schedule
plan = scheduler.build_daily_plan()
print("Today's Schedule:")
for task in plan:
    print(f"- {task.title} at {task.due_time} ({task.priority} priority, {task.duration} min)")