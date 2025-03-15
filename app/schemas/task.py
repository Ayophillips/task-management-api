from pydantic import BaseModel, Field, validator
from datetime import date, timedelta
from typing import Optional
import datetime
from app.models.task import PriorityEnum, StatusEnum

class TaskBase(BaseModel):
    """
    Base model for task management.
    
    Attributes:
        title: Task title (1-100 characters)
        description: Optional task description
        due_date: When the task is due
        priority: Task priority level (default: Medium)
        status: Current task status (default: Pending)
    """
        
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    due_date: date
    priority: PriorityEnum = PriorityEnum.MEDIUM
    status: StatusEnum = StatusEnum.PENDING

    @validator('due_date')
    def validate_due_date(cls, v):
        if v < date.today():
            raise ValueError('Due date cannot be in the past')
        if v > date.today() + timedelta(days=365):
            raise ValueError('Due date cannot be more than 1 year in the future')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Complete project documentation",
                "description": "Write comprehensive API documentation",
                "due_date": "2024-12-31",
                "priority": "MEDIUM",
                "status": "PENDING"
            }
        }

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[date] = None
    priority: Optional[PriorityEnum] = None
    status: Optional[StatusEnum] = None

    @validator('due_date')
    def validate_optional_due_date(cls, v):
        if v is not None and v < date.today():
            raise ValueError('Due date cannot be in the past')
        return v
        
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Updated documentation task",
                "status": "IN_PROGRESS"
            }
        }

class TaskResponse(TaskBase):
    id: int = Field(..., description="Unique task identifier")
    user_id: int = Field(..., description="ID of the task owner")
    created_at: datetime.datetime = Field(..., description="Task creation timestamp")
    updated_at: datetime.datetime = Field(..., description="Last update timestamp")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 123,
                "title": "Complete project documentation",
                "description": "Write comprehensive API documentation",
                "due_date": "2024-12-31",
                "priority": "MEDIUM",
                "status": "IN_PROGRESS",
                "created_at": "2024-03-13T10:00:00",
                "updated_at": "2024-03-13T10:00:00"
            }
        }
