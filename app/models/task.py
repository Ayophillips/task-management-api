from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
# from beanie import Document, Link
# from pydantic import EmailStr
import datetime
from datetime import date
from app.models.enums import PriorityEnum, StatusEnum
from sqlalchemy import UniqueConstraint

# class Task(Document):
#     title: str
#     description: Optional[str] = None
#     due_date: date
#     priority: PriorityEnum = PriorityEnum.MEDIUM
#     status: StatusEnum = StatusEnum.PENDING
#     created_at: datetime.datetime = datetime.datetime.now()
#     updated_at: datetime.datetime = datetime.datetime.now()
    
#     user_id: str
    
#     class Settings:
#         name = "tasks"
#         indexes = [
#             "title",
#             "user_id"
#         ]

class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    __table_args__ = (
        UniqueConstraint("title", "user_id", name="uq_task_title_user_id"),
    )
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, description="Task title - must be unique per user")
    description: Optional[str] = Field(default=None)
    due_date: date
    priority: PriorityEnum = Field(default=PriorityEnum.MEDIUM)
    status: StatusEnum = Field(default=StatusEnum.PENDING)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    
    user_id: int = Field(foreign_key="users.id")
    user: Optional["User"] = Relationship(back_populates="tasks")  # Use string literal for forward reference

