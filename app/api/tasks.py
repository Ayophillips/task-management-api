from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select, or_
from typing import List, Optional
import datetime
from datetime import date
import logging
# from beanie import PydanticObjectId
from app.database import get_session
from app.models.task import Task, PriorityEnum, StatusEnum
from app.models.user import User
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.core.security import get_current_active_user

logger = logging.getLogger(__name__)

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
    logger.info(f"Creating new task: {task.title} for user: {current_user.username}")
    
    # db_task = Task(
    #     **task.dict(),
    #     user_id=str(current_user.id)
    # )
    
    # await db_task.insert()
    # return db_task
    
    db_task = Task(
        **task.dict(),
        user_id=current_user.id
    )
    
    session.add(db_task)
    session.commit()
    logger.info(f"Task created successfully: ID {db_task.id}")
    session.refresh(db_task)
    
    return db_task

@router.get("/", response_model=List[TaskResponse])
def get_tasks(
    skip: int = 0,
    limit: int = 50,
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
    logger.info(f"Fetching tasks for user: {current_user.username} with filters: title={title}, status={status}, priority={priority}")

    # query = {"user_id": str(current_user.id)}
    
    # if title:
    #     query["title"] = {"$regex": title, "$options": "i"}
    # if status:
    #     query["status"] = status
    # if priority:
    #     query["priority"] = priority
        
    # tasks = await Task.find(query).skip(skip).limit(limit).to_list()

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
    logger.debug(f"Retrieved {len(tasks)} tasks for user_id={current_user.id}")
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
    logger.info(f"Fetching task_id={task_id} for user_id={current_user.id}")
    
    #  task = await Task.find_one({
    #     "_id": task_id,
    #     "user_id": str(current_user.id)
    # })

    task = session.exec(select(Task).where(Task.id == task_id, Task.user_id == current_user.id)).first()
    
    if not task:
        logger.warning(f"Task not found: task_id={task_id}, user_id={current_user.id}")
        raise HTTPException(status_code=404, detail="Task not found")
    
    logger.debug(f"Retrieved task: {task.title} (task_id={task_id})")

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
    logger.info(f"Updating task {task_id} for user: {current_user.username}")
    
    # task = await Task.find_one({
    #     "_id": task_id,
    #     "user_id": str(current_user.id)
    # })
    
    db_task = session.exec(select(Task).where(Task.id == task_id, Task.user_id == current_user.id)).first()
    
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # update_data = task_update.dict(exclude_unset=True)
    # if update_data:
    #     await task.update({"$set": update_data})
    
    # logger.info(f"Task {task_id} updated successfully")
    # return task

    # Update only the provided fields
    task_data = task_update.dict(exclude_unset=True)
    
    for key, value in task_data.items():
        setattr(db_task, key, value)
    
    # Always update the updated_at timestamp
    db_task.updated_at = datetime.datetime.now()
    
    session.add(db_task)
    session.commit()
    logger.info(f"Task {task_id} updated successfully")
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
    logger.info(f"Deleting task {task_id} for user: {current_user.username}")
    
    # delete_result = await Task.find_one({
    #     "_id": task_id,
    #     "user_id": str(current_user.id)
    # }).delete()
    
    # if not delete_result:
    #     raise HTTPException(status_code=404, detail="Task not found")
    
    # logger.info(f"Task {task_id} deleted successfully")
    
    db_task = session.exec(select(Task).where(Task.id == task_id, Task.user_id == current_user.id)).first()
    
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    session.delete(db_task)
    session.commit()
    logger.info(f"Task {task_id} deleted successfully")
    
    return None

