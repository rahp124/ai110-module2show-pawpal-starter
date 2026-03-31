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

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    st.warning(
        "Not implemented yet. Next step: create your scheduling logic (classes/functions) and call it here."
    )
    st.markdown(
        """
Suggested approach:
1. Design your UML (draft).
2. Create class stubs (no logic).
3. Implement scheduling behavior.
4. Connect your scheduler here and display results.
"""
    )
