from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from app.models.task import Task
import datetime

class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    
    tasks: List["Task"] = Relationship(back_populates="user")

