from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
import datetime
from datetime import date
from app.models.enums import PriorityEnum, StatusEnum

class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: Optional[str] = Field(default=None)
    due_date: date
    priority: PriorityEnum = Field(default=PriorityEnum.MEDIUM)
    status: StatusEnum = Field(default=StatusEnum.PENDING)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    
    user_id: int = Field(foreign_key="users.id")
    user: Optional["User"] = Relationship(back_populates="tasks")  # Use string literal for forward reference

