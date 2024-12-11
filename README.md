1. Set Up React Environment
Use create-react-app to set up a new React project:
bash
Copy code
npx create-react-app kanban-board
cd kanban-board
2. Folder Structure
Organize your project into a clean structure:

css
Copy code
src/
  components/
    KanbanBoard.js
    TaskCard.js
    TaskForm.js
    SearchBar.js
  utils/
    state.js
3. Install Dependencies
Install react-dnd and react-dnd-html5-backend for drag-and-drop functionality.
bash
Copy code
npm install react-dnd react-dnd-html5-backend
For styling, you can use libraries like Material-UI or Styled-components.
4. State Management (Using Redux or Context API)
You can use Redux for global state management. Here’s how to set it up:
bash
Copy code
npm install @reduxjs/toolkit react-redux
Create a state.js file inside the utils/ folder to manage the task data.
5. Create Components
KanbanBoard.js:

This will contain the main structure of the board.
Render columns for each task stage: To Do, In Progress, Peer Review, Done.
jsx
Copy code
import React from 'react';
import TaskCard from './TaskCard';

const KanbanBoard = ({ tasks, moveTask }) => {
    const stages = ['To Do', 'In Progress', 'Peer Review', 'Done'];

    return (
        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            {stages.map(stage => (
                <div key={stage} style={{ flex: 1, padding: '10px', border: '1px solid #ccc' }}>
                    <h3>{stage}</h3>
                    {tasks[stage].map((task, index) => (
                        <TaskCard
                            key={index}
                            task={task}
                            stage={stage}
                            moveTask={moveTask}
                        />
                    ))}
                </div>
            ))}
        </div>
    );
};

export default KanbanBoard;
TaskCard.js:

This will render individual task cards.
Implement the drag and drop functionality.
jsx
Copy code
import React from 'react';
import { useDrag, useDrop } from 'react-dnd';

const TaskCard = ({ task, stage, moveTask }) => {
    const [{ isDragging }, drag] = useDrag({
        type: 'TASK',
        item: { task, stage },
        collect: monitor => ({
            isDragging: monitor.isDragging(),
        }),
    });

    const [, drop] = useDrop({
        accept: 'TASK',
        drop: (item) => moveTask(item.task, item.stage, stage),
    });

    return (
        <div
            ref={node => drag(drop(node))}
            style={{
                opacity: isDragging ? 0.5 : 1,
                backgroundColor: '#fff',
                border: '1px solid #ddd',
                margin: '10px 0',
                padding: '10px',
                cursor: 'move',
            }}
        >
            <strong>{task.title}</strong>
            <p>{task.description}</p>
        </div>
    );
};

export default TaskCard;
SearchBar.js:

This will render the search bar and handle the filtering of tasks by title.
jsx
Copy code
import React from 'react';

const SearchBar = ({ searchTerm, setSearchTerm }) => {
    return (
        <div style={{ marginBottom: '20px' }}>
            <input
                type="text"
                placeholder="Search tasks..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                style={{ padding: '10px', width: '100%' }}
            />
        </div>
    );
};

export default SearchBar;
TaskForm.js:

This will render a form to add new tasks in the "To Do" column.
jsx
Copy code
import React, { useState } from 'react';

const TaskForm = ({ addTask }) => {
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        addTask(title, description);
        setTitle('');
        setDescription('');
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                placeholder="Task Title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
            />
            <textarea
                placeholder="Task Description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                required
            ></textarea>
            <button type="submit">Add Task</button>
        </form>
    );
};

export default TaskForm;
6. Implement Drag and Drop Logic
In KanbanBoard.js, implement the moveTask function to update the state when a task is moved between columns.
jsx
Copy code
const moveTask = (task, fromStage, toStage) => {
    const updatedTasks = { ...tasks };
    updatedTasks[fromStage] = updatedTasks[fromStage].filter(t => t !== task);
    updatedTasks[toStage].push(task);
    setTasks(updatedTasks);
};
7. Search Functionality
Inside KanbanBoard.js, filter tasks based on the search term entered in the SearchBar.js component.
jsx
Copy code
const filteredTasks = Object.keys(tasks).reduce((acc, stage) => {
    acc[stage] = tasks[stage].filter(task => task.title.toLowerCase().includes(searchTerm.toLowerCase()));
    return acc;
}, {});
8. Putting Everything Together
In App.js, combine all the components (KanbanBoard, TaskForm, SearchBar) and provide the necessary state and handlers.
jsx
Copy code
import React, { useState } from 'react';
import KanbanBoard from './components/KanbanBoard';
import TaskForm from './components/TaskForm';
import SearchBar from './components/SearchBar';

const App = () => {
    const [tasks, setTasks] = useState({
        'To Do': [
            { title: 'Task 1', description: 'Description of Task 1' },
            { title: 'Task 2', description: 'Description of Task 2' },
        ],
        'In Progress': [{ title: 'Task 3', description: 'Description of Task 3' }],
        'Peer Review': [{ title: 'Task 4', description: 'Description of Task 4' }],
        'Done': [{ title: 'Task 5', description: 'Description of Task 5' }],
    });
    const [searchTerm, setSearchTerm] = useState('');

    const addTask = (title, description) => {
        setTasks(prevTasks => ({
            ...prevTasks,
            'To Do': [...prevTasks['To Do'], { title, description }],
        }));
    };

    return (
        <div style={{ padding: '20px' }}>
            <h1>Kanban Board</h1>
            <SearchBar searchTerm={searchTerm} setSearchTerm={setSearchTerm} />
            <TaskForm addTask={addTask} />
            <KanbanBoard tasks={filteredTasks} moveTask={moveTask} />
        </div>
    );
};

export default App;
9. Styling and Responsiveness
Ensure that your layout is responsive by using CSS Flexbox or a UI library like Material-UI.
Example for Material-UI installation:
bash
Copy code
npm install @mui/material @emotion/react @emotion/styled
10. Optional Features
External Services: You can consume APIs or use Firebase for storing and retrieving tasks.
Database Integration: Use local storage or an external database to persist task data. If using a backend like Express, you can set up a REST API to manage task data.
11. Readme File
Create a README.md file to document how to set up and run the application, dependencies, and any additional features you may have added.
![image](https://github.com/user-attachments/assets/a6659482-be31-495c-8e1a-3c662b8030c8)
![image](https://github.com/user-attachments/assets/c041205c-2eef-42c6-8c04-8c5023ad509d)
![image](https://github.com/user-attachments/assets/4ef989a4-8440-4054-9e21-12ba5278172b)




