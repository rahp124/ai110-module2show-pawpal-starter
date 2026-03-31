import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

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

# Initialize Owner in session_state
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")

st.subheader("Pet Management")

# Form to add a new pet
with st.form("add_pet_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        pet_name = st.text_input("Pet name", value="Mochi")
    
    with col2:
        species = st.selectbox("Species", ["dog", "cat", "bird", "rabbit", "hamster", "other"])
    
    age = st.number_input("Age (years)", min_value=0, max_value=50, value=2, step=1)
    
    submit_button = st.form_submit_button("Add Pet")
    
    if submit_button:
        # Create new Pet instance and add to Owner
        new_pet = Pet(name=pet_name, species=species, age=age)
        st.session_state.owner.add_pet(new_pet)
        st.success(f"✅ Added {pet_name} the {species}!")

# Display current pets
st.subheader("Current Pets")
current_pets = st.session_state.owner.get_pets()

if current_pets:
    pet_data = [
        {
            "Name": pet.name,
            "Species": pet.species,
            "Age": f"{pet.age} year{'s' if pet.age != 1 else ''}",
            "Tasks": len(pet.get_tasks())
        }
        for pet in current_pets
    ]
    st.table(pet_data)
else:
    st.info("No pets yet. Add one using the form above!")

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    st.session_state.tasks.append(
        {"title": task_title, "duration_minutes": int(duration), "priority": priority}
    )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("📅 Daily Schedule")
st.caption("View and manage your pet care schedule with conflict detection.")

# Initialize scheduler
scheduler = Scheduler()

# Pet filter selector
col1, col2 = st.columns([2, 1])
with col1:
    all_pets = [pet.name for pet in st.session_state.owner.get_pets()]
    selected_pet_filter = st.selectbox(
        "Filter by pet", 
        ["All Pets"] + all_pets
    )

# Task status filter
with col2:
    task_status = st.selectbox("Status", ["Pending", "Completed", "All"])

# Get tasks based on filters
if selected_pet_filter == "All Pets":
    if task_status == "Pending":
        filtered_tasks = scheduler.filter_tasks_by_completion(st.session_state.owner, False)
    elif task_status == "Completed":
        filtered_tasks = scheduler.filter_tasks_by_completion(st.session_state.owner, True)
    else:
        filtered_tasks = st.session_state.owner.get_all_tasks(include_completed=True)
else:
    pet_tasks = scheduler.filter_tasks_by_pet_name(st.session_state.owner, selected_pet_filter)
    if task_status == "Pending":
        filtered_tasks = [t for t in pet_tasks if not t.is_completed]
    elif task_status == "Completed":
        filtered_tasks = [t for t in pet_tasks if t.is_completed]
    else:
        filtered_tasks = pet_tasks

# Sort tasks by scheduled time
sorted_tasks = sorted(
    filtered_tasks,
    key=lambda t: t.scheduled_time if t.scheduled_time else "99:99"
)

# Display schedule
if sorted_tasks:
    st.success(f"✅ Showing {len(sorted_tasks)} task(s)")
    
    # Create schedule table
    schedule_data = []
    for task in sorted_tasks:
        pet_name = next(
            (pet.name for pet in st.session_state.owner.get_pets() if task in pet.get_tasks()),
            "Unknown"
        )
        schedule_data.append({
            "Time": task.scheduled_time or "—",
            "Pet": pet_name,
            "Task": task.description,
            "Duration (min)": task.time_minutes,
            "Priority": "🔴 High" if task.priority >= 3 else "🟡 Medium" if task.priority >= 2 else "🟢 Low",
            "Status": "✓ Done" if task.is_completed else "⏳ Pending"
        })
    
    st.table(schedule_data)
    
    # Check for conflicts in selected pet
    if selected_pet_filter != "All Pets":
        selected_pet = next(
            (pet for pet in st.session_state.owner.get_pets() if pet.name == selected_pet_filter),
            None
        )
        
        if selected_pet and len(selected_pet.get_tasks()) > 0:
            st.markdown("**⚠️ Checking for scheduling conflicts...**")
            
            # Find time-based conflicts
            scheduled_times = {}
            conflicts_found = False
            
            for task in selected_pet.get_tasks():
                if task.scheduled_time:
                    if task.scheduled_time in scheduled_times:
                        conflicts_found = True
                        st.warning(
                            f"⏰ **Conflict at {task.scheduled_time}**: "
                            f"'{scheduled_times[task.scheduled_time]}' and '{task.description}' are both scheduled at the same time."
                        )
                    else:
                        scheduled_times[task.scheduled_time] = task.description
            
            if not conflicts_found:
                st.success(f"✓ No scheduling conflicts detected for {selected_pet_filter}!")
else:
    st.info("No tasks to display. Add tasks above and assign scheduled times to see your schedule.")

st.divider()

st.subheader("Build Schedule (Automatic Planning)")
st.caption("Generate an optimal daily plan based on available time.")

available_minutes = st.slider("Available time (minutes)", min_value=30, max_value=480, value=120)

if st.button("Generate schedule"):
    daily_plan = scheduler.generate_daily_plan(st.session_state.owner, available_minutes)
    
    if daily_plan:
        total_time = sum(task.time_minutes for task in daily_plan)
        st.success(f"✅ Generated plan with {len(daily_plan)} tasks ({total_time} minutes)")
        
        plan_data = []
        for task in daily_plan:
            plan_data.append({
                "Task": task.description,
                "Duration": f"{task.time_minutes} min",
                "Priority": "🔴 High" if task.priority >= 3 else "🟡 Medium" if task.priority >= 2 else "🟢 Low",
                "Frequency": task.frequency
            })
        
        st.table(plan_data)
    else:
        st.warning("No tasks fit in the available time. Try adding tasks or increasing available time.")
