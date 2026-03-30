import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Initialize Owner in session_state
if 'owner' not in st.session_state:
    st.session_state.owner = Owner(
        name="Jordan",  # Default, can be updated
        available_time="9am-5pm",
        preferences={"theme": "light"}
    )

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Manage Pets")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
age = st.number_input("Age", min_value=0, max_value=30, value=2)

if st.button("Add Pet"):
    pet = Pet(name=pet_name, species=species, age=age)
    st.session_state.owner.add_pet(pet)
    st.success(f"Added {pet_name} to your pets!")
    st.rerun()  # Refresh to update UI

if st.session_state.owner.pets:
    st.write("Your Pets:")
    for pet in st.session_state.owner.pets:
        st.write(f"- {pet.name} ({pet.species}, {pet.age} years old)")
        if pet.tasks:
            st.write("  Tasks:")
            for task in pet.tasks:
                st.write(f"    - {task.title} ({task.priority}, {task.due_time})")
else:
    st.info("No pets added yet.")

st.markdown("### Add Tasks")
st.caption("Add tasks to your pets.")

if st.session_state.owner.pets:
    pet_names = [p.name for p in st.session_state.owner.pets]
    selected_pet = st.selectbox("Select pet to add task to", pet_names)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col4:
        due_time = st.text_input("Due time (HH:MM)", value="08:00")
    
    if st.button("Add Task"):
        pet = st.session_state.owner.get_pet_by_name(selected_pet)
        if pet:
            task = Task(
                title=task_title,
                category="general",  # Default
                duration=duration,
                priority=priority,
                due_time=due_time,
                due_date="2026-03-30",  # Today's date
                frequency="daily",
                notes=""
            )
            pet.add_task(task)
            st.success(f"Added {task_title} to {selected_pet}!")
            st.rerun()
else:
    st.info("Add a pet first to add tasks.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate your daily schedule based on tasks.")

if st.button("Generate Schedule"):
    scheduler = Scheduler(st.session_state.owner)
    plan = scheduler.build_daily_plan()
    explanation = scheduler.explain_choices()
    
    # Check for conflicts
    all_tasks = st.session_state.owner.get_all_tasks()
    conflicts = scheduler.detect_conflicts(all_tasks)
    if conflicts:
        for warning in conflicts:
            st.warning(warning)
    
    if plan:
        st.success("Daily Plan Generated!")
        # Sort by time for display
        sorted_plan = scheduler.sort_by_time(plan)
        # Display as table
        plan_data = [
            {"Task": task.title, "Time": task.due_time, "Priority": task.priority, "Duration (min)": task.duration}
            for task in sorted_plan
        ]
        st.table(plan_data)
        st.write("**Explanation:**", explanation)
    else:
        st.info("No tasks due today.")
