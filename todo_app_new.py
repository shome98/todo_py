import streamlit as st
import uuid
st.set_page_config(page_title="New Todo using stramlit",layout="centered")

def initialize_state():
    if 'tasks' not in st.session_state:
        st.session_state.tasks=[]

def add_task(new_task_description):
    if new_task_description:
        st.session_state.tasks.append({
            'id':str(uuid.uuid4()),
            'description': new_task_description,
            'done': False
        })
    else:
        st.warning("😡😡😡 Please enter something!!!")
def display_tasks():
    if not st.session_state.tasks:
        st.info("😒 Your todo list is empty. 😊 Add some tasks to continue.")
        return
    st.subheader("😊 Your Tasks")
    tasks_changed=False
    indices_to_delete=[]
    for i in range(len(st.session_state.tasks)):
        task=st.session_state.tasks[i]
        task_id=task['id']
        col1,col2=st.columns([0.8,0.2])
        with col1:
            is_done=st.checkbox(
                task['description'],
                value=task['done'],
                key=f"cb_{task_id}"
            )
            if is_done!=task['done']:
                st.session_state.tasks[i]['done']=is_done
                tasks_changed=True
        with col2:
            if st.button("❌ Delete",key=f"del_{task_id}"):
                indices_to_delete.append(i)
                tasks_changed=True
    if indices_to_delete:
        for index in sorted(indices_to_delete,reverse=True):
            deleted_task=st.session_state.tasks.pop(index)
            st.success(f"Deleted task: {deleted_task['description']}")
    if tasks_changed:
        st.rerun()


initialize_state()
st.title("📝 Todo app with streamlit")
st.header("😊 Add a New Task")
new_task_description_input=st.text_input(
    "Enter task description: ",
    placeholder="😊 E.g., Play..."
)
if st.button("😊 Add Task",key="add_button"):
    add_task(new_task_description_input)
    st.rerun()
st.divider()
display_tasks()