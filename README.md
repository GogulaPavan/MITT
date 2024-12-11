                                  **Assignment 1**
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

       **Assignment 2**

       This Streamlit code fetches product data from the provided API (https://fakestoreapi.com/), displays products on the homepage, supports product search, and allows users to add/remove items from a cart.

Install Required Libraries
Before running the code, ensure you have the necessary libraries:

bash
Copy code
pip install streamlit requests
Streamlit Code
python
Copy code
import streamlit as st
import requests
import pandas as pd
from typing import List

# Fetch products from API
def fetch_products(page: int = 1, limit: int = 10) -> List[dict]:
    url = f"https://fakestoreapi.com/products?limit={limit}&page={page}"
    response = requests.get(url)
    return response.json()

# Display product details on product detail page
def display_product_details(product_id: int):
    product = next(p for p in products if p['id'] == product_id)
    st.image(product['image'], width=300)
    st.title(product['title'])
    st.subheader(f"Price: ${product['price']}")
    st.text(f"Description: {product['description']}")
    st.text(f"Rating: {product['rating']['rate']} stars")
    st.text(f"Reviews: {product['rating']['count']} reviews")
    st.button("Add to Cart", on_click=add_to_cart, args=(product,))

# Function to add products to the cart
def add_to_cart(product):
    cart.append(product)
    st.success(f"Added {product['title']} to the cart")

# Display the cart
def display_cart():
    if not cart:
        st.warning("Your cart is empty!")
        return
    st.header("Your Cart")
    total_price = 0
    for product in cart:
        st.image(product['image'], width=50)
        st.write(f"{product['title']} - ${product['price']}")
        total_price += product['price']
    st.write(f"Total Price: ${total_price}")
    st.button("Proceed to Checkout", on_click=checkout)

# Checkout functionality
def checkout():
    st.write("Proceeding to checkout...")
    st.write("Thank you for your purchase!")

# Main app layout
st.title("E-Commerce Store")
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose page", ["Homepage", "Cart"])

# Global cart variable to store selected products
if 'cart' not in st.session_state:
    st.session_state.cart = []

cart = st.session_state.cart

if page == "Homepage":
    st.header("Featured Products")
    products = fetch_products(page=1)
    for product in products:
        st.image(product['image'], width=100)
        st.subheader(product['title'])
        st.write(f"Price: ${product['price']}")
        st.write(f"Rating: {product['rating']['rate']} stars")
        if st.button(f"View {product['title']} details", key=product['id']):
            display_product_details(product['id'])
        if st.button(f"Add {product['title']} to cart", key=f"add_{product['id']}"):
            add_to_cart(product)

elif page == "Cart":
    display_cart()
Explanation of the Code
Homepage:

fetch_products: Fetches products from the FakeStoreAPI.
Displaying Products: On the homepage, the app shows a list of products with their images, titles, prices, and ratings.
Add to Cart: The "Add to Cart" button allows users to add products to their cart.
Product Detail Page:

display_product_details: Displays detailed information about the selected product.
Add to Cart in Detail Page: From the product detail page, users can also add the product to their cart.
Cart:

display_cart: Displays the contents of the cart with product names, prices, and images.
Checkout: When users press the "Proceed to Checkout" button, a simple confirmation message is shown.
State Management (Session State):

The cart is stored in st.session_state, which allows persisting the cart's data across interactions.
How to Run the Application
Copy the code into a Python file, for example, ecommerce_app.py.
Run the Streamlit app using the command:
bash
Copy code
streamlit run ecommerce_app.py
This will open the application in your browser.

Key Features
Infinite Scrolling: You can extend this by loading additional products as the user scrolls down (implement pagination in the API calls).
Search: You can add a search bar to filter products by name.
User Authentication: For authentication, you could integrate a third-party service like Firebase or use a local form with basic validation.
Product Sorting and Filtering: Sorting by price or rating can be implemented using sort() functions, and filtering can be done by adding relevant checkboxes or sliders for categories and price ranges.
Best Practices
Use st.session_state for managing user data (like cart).
State Management: The app is using Streamlit's built-in session state to keep track of the cart, making it simple to implement without additional state management libraries.
Separation of Concerns: The business logic is separated into functions (e.g., fetching products, displaying details, adding to cart) to maintain a clean architecture.

![image](https://github.com/user-attachments/assets/c73ae9c7-55ca-441a-ae86-3ffca924ad13)
![image](https://github.com/user-attachments/assets/3dfbe9de-cb5a-48a4-b9ee-811c8c957f12)
![image](https://github.com/user-attachments/assets/35c13178-e1e0-4ff8-bbb1-cd927d46aeda)



  




