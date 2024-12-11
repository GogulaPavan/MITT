import streamlit as st
import streamlit.components.v1 as components
import json

# Sample tasks
tasks = {
    "To Do": [
        {"title": "Task 1", "description": "Description of Task 1"},
        {"title": "Task 2", "description": "Description of Task 2"},
    ],
    "In Progress": [
        {"title": "Task 3", "description": "Description of Task 3"},
    ],
    "Peer Review": [
        {"title": "Task 4", "description": "Description of Task 4"},
    ],
    "Done": [
        {"title": "Task 5", "description": "Description of Task 5"},
    ],
}

# Convert tasks to JSON for JavaScript rendering
def generate_task_data(tasks):
    return json.dumps(tasks)

def render_html_kanban(task_data):
    kanban_html = f"""
    <div id='search-bar' style='margin-bottom: 20px;'>
        <input type='text' id='search-input' placeholder='Search tasks...' style='width: 100%; padding: 8px; margin-bottom: 10px;' />
    </div>
    <div id='kanban-board' style='display: flex; gap: 10px;'></div>
    <script>
        const tasks = {task_data};
        const board = document.getElementById('kanban-board');
        const stages = ['To Do', 'In Progress', 'Peer Review', 'Done'];

        // Generate columns for each stage
        stages.forEach(stage => {{
            const column = document.createElement('div');
            column.style.border = '1px solid #ccc';
            column.style.padding = '10px';
            column.style.margin = '10px';
            column.style.flex = '1';
            column.style.minHeight = '300px';
            column.style.backgroundColor = '#f1f1f1';
            column.innerHTML = `<h3>${{stage}}</h3>`;
            column.id = stage.replace(/\\s+/g, '-');
            column.setAttribute('ondrop', 'drop(event)');
            column.setAttribute('ondragover', 'allowDrop(event)');

            if (tasks[stage]) {{
                tasks[stage].forEach((task, index) => {{
                    const taskCard = document.createElement('div');
                    taskCard.style.border = '1px solid #aaa';
                    taskCard.style.margin = '5px';
                    taskCard.style.padding = '10px';
                    taskCard.style.backgroundColor = '#f9f9f9';
                    taskCard.setAttribute('draggable', 'true');
                    taskCard.setAttribute('ondragstart', 'drag(event)');
                    taskCard.id = 'task-' + index;
                    taskCard.innerHTML = `<strong>${{task.title}}</strong><br><p>${{task.description}}</p>`;
                    column.appendChild(taskCard);
                }});
            }}

            board.appendChild(column);
        }});

        // Drag-and-Drop Functions
        function allowDrop(ev) {{
            ev.preventDefault();
        }}

        function drag(ev) {{
            ev.dataTransfer.setData('text', ev.target.id);
        }}

        function drop(ev) {{
            ev.preventDefault();
            var data = ev.dataTransfer.getData('text');
            var taskCard = document.getElementById(data);
            var targetColumn = ev.target;
            
            if (targetColumn.id !== taskCard.parentElement.id && targetColumn.id !== 'kanban-board') {{
                targetColumn.appendChild(taskCard);
            }}
        }}

        // Search Functionality
        const searchInput = document.getElementById('search-input');
        searchInput.addEventListener('input', function() {{
            const searchTerm = searchInput.value.toLowerCase();
            stages.forEach(stage => {{
                const column = document.getElementById(stage.replace(/\\s+/g, '-'));
                const taskCards = column.querySelectorAll('div');
                taskCards.forEach(taskCard => {{
                    const title = taskCard.querySelector('strong').innerText.toLowerCase();
                    if (title.includes(searchTerm)) {{
                        taskCard.style.display = 'block';
                    }} else {{
                        taskCard.style.display = 'none';
                    }}
                }});
            }});
        }});
    </script>
    """

    return kanban_html

# Streamlit application
st.set_page_config(layout="wide")
st.title("Kanban Board with Streamlit")

# Input for adding new tasks
st.sidebar.header("Add New Task")
new_task_title = st.sidebar.text_input("Task Title")
new_task_description = st.sidebar.text_area("Task Description")

if st.sidebar.button("Add Task"):
    if new_task_title and new_task_description:
        tasks["To Do"].append({"title": new_task_title, "description": new_task_description})
        st.sidebar.success("Task added to 'To Do'.")
    else:
        st.sidebar.error("Please enter both title and description.")

# Render Kanban board
st.markdown("### Kanban Board")
components.html(render_html_kanban(generate_task_data(tasks)), height=600)
