from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select, or_
from typing import List, Optional
import datetime
from datetime import date

from app.database import get_session
from app.models.task import Task, PriorityEnum, StatusEnum
from app.models.user import User
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.core.security import get_current_active_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new task.
    
    - **title**: Required. The task title
    - **description**: Optional. Task description
    - **due_date**: Required. When the task is due (YYYY-MM-DD)
    - **priority**: Optional. Task priority (Low/Medium/High)
    - **status**: Optional. Task status (Pending/Completed)
    """
    db_task = Task(
        **task.dict(),
        user_id=current_user.id
    )
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    
    return db_task

@router.get("/", response_model=List[TaskResponse])
def get_tasks(
    skip: int = 0,
    limit: int = 100,
    title: Optional[str] = None,
    description: Optional[str] = None,
    due_date: Optional[date] = None,
    status: Optional[StatusEnum] = None,
    priority: Optional[PriorityEnum] = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all tasks for the current user.
    
    Supports filtering by title, status, and priority.
    """
    query = select(Task).where(Task.user_id == current_user.id)
    
    # Apply filters if provided
    if title:
        query = query.where(Task.title.contains(title))
    if description:  
        query = query.where(Task.description.contains(description))
    if due_date:     
        query = query.where(Task.due_date == due_date)
    if status:
        query = query.where(Task.status == status)
    if priority:
        query = query.where(Task.priority == priority)
    
    # Apply pagination
    query = query.offset(skip).limit(limit)
    
    tasks = session.exec(query).all()
    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific task by its ID.
    """
    task = session.exec(select(Task).where(Task.id == task_id, Task.user_id == current_user.id)).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update a specific task by its ID.
    
    Only provide the fields you want to update.
    """
    db_task = session.exec(select(Task).where(Task.id == task_id, Task.user_id == current_user.id)).first()
    
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update only the provided fields
    task_data = task_update.dict(exclude_unset=True)
    
    for key, value in task_data.items():
        setattr(db_task, key, value)
    
    # Always update the updated_at timestamp
    db_task.updated_at = datetime.datetime.now()
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    
    return db_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a specific task by its ID.
    """
    db_task = session.exec(select(Task).where(Task.id == task_id, Task.user_id == current_user.id)).first()
    
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    session.delete(db_task)
    session.commit()
    
    return None

