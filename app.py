from datetime import time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+, a daily care planner for your pets.

This app is connected to the PawPal+ Python backend. Add your pets, give each one care tasks
with a duration, priority, and due time, then generate a schedule that fits the time you have
today. Higher-priority tasks are chosen first, and anything that doesn't fit is listed as skipped.
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

PRIORITY_VALUES = {"Low": 1, "Medium": 2, "High": 3}
PRIORITY_LABELS = {value: label for label, value in PRIORITY_VALUES.items()}

# --- Owner -------------------------------------------------------------------
# Streamlit reruns this script on every interaction, so the Owner is created
# once and kept in session_state. Pets live in owner.pets, tasks in pet.tasks.

st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name)
owner: Owner = st.session_state.owner
owner.name = owner_name

# --- Pets --------------------------------------------------------------------

st.subheader("Pets")

with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    age = st.number_input("Age (years)", min_value=0, max_value=40, value=3)
    add_pet_clicked = st.form_submit_button("Add pet")

if add_pet_clicked:
    name = pet_name.strip()
    if not name:
        st.error("Please enter a pet name.")
    elif any(pet.name.lower() == name.lower() for pet in owner.pets):
        st.warning(f"{owner.name} already has a pet named {name}.")
    else:
        owner.add_pet(Pet(name, species, int(age)))
        st.success(f"Added {name}.")

if owner.pets:
    st.table(
        [{"Name": pet.name, "Species": pet.species, "Age": pet.age, "Tasks": len(pet.tasks)}
         for pet in owner.pets]
    )
else:
    st.info("No pets yet. Add one above.")

# --- Tasks -------------------------------------------------------------------

st.markdown("### Tasks")

if not owner.pets:
    st.caption("Add a pet first, then you can give it tasks.")
else:
    with st.form("add_task_form", clear_on_submit=True):
        pet_index = st.selectbox(
            "Pet",
            range(len(owner.pets)),
            format_func=lambda i: owner.pets[i].name,
        )
        col1, col2 = st.columns(2)
        with col1:
            task_title = st.text_input("Task name", value="Morning walk")
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        with col2:
            priority = st.selectbox("Priority", list(PRIORITY_VALUES), index=2)
            due = st.time_input("Due time", value=time(8, 0))
        add_task_clicked = st.form_submit_button("Add task")

    if add_task_clicked:
        title = task_title.strip()
        if not title:
            st.error("Please enter a task name.")
        else:
            pet = owner.pets[pet_index]
            pet.add_task(
                Task(
                    name=title,
                    duration=int(duration),
                    priority=PRIORITY_VALUES[priority],
                    due_time=due.strftime("%H:%M"),
                )
            )
            st.success(f"Added '{title}' for {pet.name}.")

# Tasks don't store their pet, so look it up by object identity for display.
pet_name_by_task = {id(task): pet.name for pet in owner.pets for task in pet.tasks}


def task_row(task: Task) -> dict:
    """Format a task as a table row for display."""
    return {
        "Time": task.due_time,
        "Pet": pet_name_by_task.get(id(task), "?"),
        "Task": task.name,
        "Duration (min)": task.duration,
        "Priority": PRIORITY_LABELS.get(task.priority, task.priority),
    }


all_tasks = owner.get_all_tasks()
if all_tasks:
    st.write("Current tasks:")
    st.table([task_row(task) for task in sorted(all_tasks, key=lambda t: t.due_time)])
elif owner.pets:
    st.info("No tasks yet. Add one above.")

st.divider()

# --- Schedule ----------------------------------------------------------------

st.subheader("Build Schedule")
available_minutes = st.number_input(
    "Available minutes today", min_value=0, max_value=1440, value=60, step=5
)

if st.button("Generate schedule"):
    pending = [task for task in all_tasks if not task.completed]
    if not pending:
        st.info("There are no incomplete tasks to schedule. Add some tasks above.")
    else:
        plan = Scheduler(owner).generate_schedule(int(available_minutes))

        if plan:
            used = sum(task.duration for task in plan)
            st.success(f"Today's Schedule: {len(plan)} task(s), {used} of {available_minutes} minutes used.")
            st.table([task_row(task) for task in plan])
        else:
            st.warning("None of the tasks fit within the available time.")

        planned_ids = {id(task) for task in plan}
        skipped = [task for task in pending if id(task) not in planned_ids]
        if skipped:
            st.markdown("**Skipped (not enough time left):**")
            st.table([task_row(task) for task in sorted(skipped, key=lambda t: t.due_time)])
