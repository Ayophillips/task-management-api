from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
# from beanie import Document, Link
# from pydantic import EmailStr
from app.models.task import Task
import datetime


# class User(Document):
#     email: EmailStr
#     username: str
#     hashed_password: str
#     is_active: bool = True
#     created_at: datetime.datetime = datetime.datetime.now()
    
#     tasks: List[Link[Task]] = []
    
#     class Settings:
#         name = "users"
#         indexes = [
#             "email",
#             "username"
#         ]

class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    
    tasks: List["Task"] = Relationship(back_populates="user")

