# Task Management API

A RESTful API for a Task Management System built with FastAPI and SQLModel.

## Features

- User authentication with JWT
- CRUD operations for tasks
- Input validation
- Error handling
- Database ation with PostgreSQL
- API documentation with Swagger

## Tech Stack

- **Backend**: FastAPI with SQLModel
- **Database**: PostgreSQL
- **Authentication**: JWT
- **Documentation**: Swagger (built-in with FastAPI)

## Setup Instructions

### Prerequisites

- Python 3.8+
- PostgreSQL

### Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/task-management-api.git
cd task-management-api
```

2. Create a virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. a. Copy the environment template:
   ```bash
   cp .env.example .env
   ```
   b. Update the `.env` file with your local settings


5. Start the application:
```
uvicorn app.main:app --reload
```

6. Access the API documentation at `http://localhost:8000/docs`

## API Endpoints

### Authentication

- `POST /register` - Register a new user
- `POST /token` - Login and get access token
- `GET /users/me` - Get current user information

### Tasks

- `GET /tasks` - Get all tasks (with optional filtering)
- `POST /tasks` - Create a new task
- `GET /tasks/{task_id}` - Get a specific task
- `PUT /tasks/{task_id}` - Update a specific task
- `DELETE /tasks/{task_id}` - Delete a specific task

## Database Schema

The API uses two main models:

1. **User**:
- id (primary key)
- email (unique)
- username (unique)
- hashed_password
- is_active
- created_at

2. **Task**:
- id (primary key)
- title
- description
- due_date
- priority (Low/Medium/High)
- status (Pending/Completed)
- created_at
- updated_at
- user_id (foreign key)

## Testing

Run tests using pytest:
```
pytest
```

## License

This project is licensed under the MIT License.
