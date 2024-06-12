# TODO API
This is a RESTful API for a ToDo list application built using FastAPI. The application allows users to register, authenticate, and manage their tasks (CRUD operations). The API is secured with token-based authentication using JSON Web Tokens (JWT).

# Objective
Develop a RESTful API for a ToDo list application with the following features:
- Add new tasks
- Remove tasks
- Update tasks
- User authentication and secure endpoints

# Features
- User Registration
- User Authentication with JWT
- Create, Read, Update, and Delete (CRUD) tasks
- Secure password hashing using passlib
- SQLite database for storage

# Requirements
- Language and Framework: Python with FastAPI
- Database: SQLite
- ORM: SQLAlchemy
- Authentication: JSON Web Tokens (JWT)

# API Endpoints
- POST /register: Register a new user
- POST /login: Authenticate a user and return a JWT token
- GET /tasks: Retrieve the list of all tasks (authentication required)
- POST /tasks: Add a new task (authentication required)
- PUT /tasks/{task_id}: Update an existing task (authentication required)
- DELETE /tasks/{task_id}: Remove a task (authentication required)
- GET /tasks/{task_id}: Retrieve a task by id

## Installation

1. Clone the repository
```sh
git clone <repository-url>
cd todo_api
```

2. Create a virtual environment
```sh
python -m venv venv
cd todo_api
```

3. Activate the virtual environment
```sh
.\venv\Scripts\activate
```

4. Install the dependencies
```sh
pip install -r requirements.txt
```

## Running the application

1. Start the FastAPI server
```sh
uvicorn app.main:app --reload
```

2. Access the API documentation
   
Open your browser and navigate to http://127.0.0.1:8000/docs to view the interactive Swagger UI documentation.

Alternatively, you can access ReDoc at http://127.0.0.1:8000/redoc.

3. Testing
   
   i. Swagger UI
   
   ii. Postman
