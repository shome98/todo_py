import streamlit as st

# Set page configuration for a cleaner look
st.set_page_config(page_title="Simple To-Do App", layout="centered")

# Function to initialize session state for tasks if it doesn't exist
def initialize_state():
    """Initializes the session state variables if they don't exist."""
    if 'tasks' not in st.session_state:
        # Each task will be a dictionary: {'description': str, 'done': bool}
        st.session_state.tasks = []

# Function to add a new task
def add_task(new_task_description):
    """Adds a new task to the list if the description is not empty."""
    if new_task_description: # Only add if the input is not empty
        st.session_state.tasks.append({'description': new_task_description, 'done': False})
    else:
        st.warning("Please enter a task description.") # Show a warning if input is empty

# Function to display tasks and handle interactions
def display_tasks():
    """Displays tasks with checkboxes and delete buttons."""
    if not st.session_state.tasks:
        st.info("Your to-do list is empty. Add some tasks!")
        return # Exit if no tasks

    st.subheader("Your Tasks")

    # Iterate through tasks with index for deletion and updates
    tasks_to_keep = []
    deleted_task = False # Flag to rerun if a task is deleted

    for i, task in enumerate(st.session_state.tasks):
        col1, col2 = st.columns([0.8, 0.2]) # Create columns for layout

        with col1:
            # Checkbox for marking task as done/undone
            # The key is unique for each checkbox based on its index
            is_done = st.checkbox(
                task['description'],
                value=task['done'],
                key=f"task_{i}"
            )
            # Update the task's 'done' status in the original list if changed
            if is_done != task['done']:
                 st.session_state.tasks[i]['done'] = is_done
                 st.rerun() # Rerun to immediately reflect the change visually


        with col2:
            # Button to delete a task
            # The key is unique for each delete button
            if st.button("Delete", key=f"delete_{i}"):
                # Don't add this task to the `tasks_to_keep` list
                deleted_task = True # Set flag
                st.success(f"Deleted task: {task['description']}") # Confirmation message
            else:
                # If not deleted, add it to the list of tasks to keep
                tasks_to_keep.append(task)

    # Update the session state only with the tasks that were not deleted
    if deleted_task:
        st.session_state.tasks = tasks_to_keep
        st.rerun() # Rerun the script to update the display after deletion

# --- App Execution ---

# Initialize session state
initialize_state()

# App Title
st.title("📝 Simple To-Do App")

# Input field for adding new tasks
st.header("Add a New Task")
new_task = st.text_input("Enter task description:", key="new_task_input", placeholder="E.g., Buy groceries")

# Button to add the task
if st.button("Add Task", key="add_button"):
    add_task(new_task)
    # Clear the input field after adding by resetting the widget's value via key
    st.session_state.new_task_input = ""
    st.rerun() # Rerun to update the list immediately

# Display separator
st.divider()

# Display the current tasks
display_tasks()

# Optional: Display raw state for debugging (can be commented out)
# st.subheader("Session State (for debugging):")
# st.write(st.session_state.tasks)
