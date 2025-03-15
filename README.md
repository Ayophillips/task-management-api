# Task Management API

A RESTful API for a Task Management System built with FastAPI and SQLModel, deployed on Render with Supabase PostgreSQL database.

## Features

- User authentication with JWT
- CRUD operations for tasks
- Input validation and error handling
- Database integration with PostgreSQL
- API documentation with Swagger UI
- Health check endpoint
- Deployment on Render
- Database hosting on Supabase
- SSL-enabled secure connections
- Comprehensive error handling
- Logging system

## Tech Stack

- **Backend**: FastAPI 0.100.0+ with SQLModel
- **Database**: PostgreSQL 15+ (hosted on Supabase)
- **Authentication**: JWT tokens
- **Documentation**: Swagger UI (built-in with FastAPI)
- **Deployment**: Render
- **Database Hosting**: Supabase
- **SSL**: TLS 1.3

## Local Development Setup

### Prerequisites

- Python 3.8+
- PostgreSQL 14+ (local instance for development)
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/task-management-api.git
cd task-management-api
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```

5. Update `.env` with your settings:
```ini
# App settings
PROJECT_NAME="Task Management API"
PROJECT_VERSION="1.0.0"
DEBUG=True

# Database settings
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=task_management

# Security
SECRET_KEY=your-secret-key
```

6. Start the application:
```bash
uvicorn app.main:app --reload
```

7. Access the API documentation at `http://localhost:8000/docs`

## Production Deployment

### Supabase Database Setup

1. Create a Supabase account at https://supabase.com
2. Create a new project
3. Get your database credentials from Settings > Database
4. Note your connection string:
```
postgresql://postgres.[PROJECT_REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:5432/postgres
```

### Render Deployment

1. Create a Render account at https://render.com
2. Connect your GitHub repository
3. Create a new Web Service
4. Configure the following:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   
5. Add environment variables:
```ini
POSTGRES_USER=postgres.[PROJECT_REF]
POSTGRES_PASSWORD=your-supabase-password
POSTGRES_SERVER=aws-0-[REGION].pooler.supabase.com
POSTGRES_PORT=5432
POSTGRES_DB=postgres
SECRET_KEY=your-production-secret-key
```

### Verifying Deployment

1. Check the health endpoint:
```bash
curl https://your-app-name.onrender.com/health
```

2. Monitor logs in Render dashboard

## API Endpoints

### Authentication
- `POST /register` - Register a new user
- `POST /token` - Login and get access token
- `GET /users/me` - Get current user information

### Tasks
- `GET /tasks` - Get all tasks (with filtering)
- `POST /tasks` - Create a new task
- `GET /tasks/{task_id}` - Get a specific task
- `PUT /tasks/{task_id}` - Update a task
- `DELETE /tasks/{task_id}` - Delete a task

### System
- `GET /health` - Check system health
- `GET /` - API information

## Database Schema

### User Model
- `id`: Integer (primary key)
- `email`: String (unique)
- `username`: String (unique)
- `hashed_password`: String
- `is_active`: Boolean
- `created_at`: DateTime

### Task Model
- `id`: Integer (primary key)
- `title`: String (unique per user)
- `description`: String (optional)
- `due_date`: Date
- `priority`: Enum (Low/Medium/High)
- `status`: Enum (Pending/Completed)
- `created_at`: DateTime
- `updated_at`: DateTime
- `user_id`: Integer (foreign key)

## Testing

Run the test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app tests/
```

## Monitoring

- Health checks available at `/health`
- Logs available in Render dashboard
- Database metrics in Supabase dashboard

## License

This project is licensed under the MIT License.
