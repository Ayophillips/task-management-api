from pydantic import BaseModel, EmailStr, Field, constr
from typing import Optional, Pattern
from datetime import datetime

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class UserBase(BaseModel):
    """
    Base model for user management.
    
    Attributes:
        email: User's email address (must be valid format)
        username: Username (3-50 characters, alphanumeric and underscores only)
    """
    email: EmailStr = Field(
        ...,
        description="User's email address",
        example="user@example.com"
    )
    username: constr(min_length=3, max_length=50, pattern=r'^[a-zA-Z0-9_]+$') = Field( # type: ignore
        ...,
        description="Username (alphanumeric and underscores only)",
        example="john_doe123"
    )

class UserCreate(UserBase):
    """Model for user registration."""
    password: str = Field(
        ...,
        description="User password (8-50 characters)",
        example="SecurePass123!",
        min_length=8,
        max_length=50
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "john_doe123",
                "password": "SecurePass123!"
            }
        }

class UserResponse(UserBase):
    """Model for user data responses."""
    # id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    # is_active: bool = Field(default=True)
    id: int = Field(..., description="Unique user identifier")
    is_active: bool = Field(..., description="User account status")
    created_at: datetime = Field(..., description="Account creation timestamp")
    
    # class Config:
    #     json_encoders = {
    #         ObjectId: str
    #     }
    #     allow_population_by_field_name = True
    #     schema_extra = {
    #         "example": {
    #             "_id": "507f1f77bcf86cd799439011",
    #             "email": "user@example.com",
    #             "username": "john_doe123",
    #             "is_active": True,
    #             "created_at": "2024-03-13T10:00:00"
    #         }
    #     }

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "user@example.com",
                "username": "john_doe123",
                "is_active": True,
                "created_at": "2024-03-13T10:00:00"
            }
        }

class Token(BaseModel):
    """Authentication token model."""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(..., description="Token type (usually 'bearer')")
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }

class TokenData(BaseModel):
    """Token payload data model."""
    username: Optional[str] = Field(
        None,
        description="Username stored in the token",
        example="john_doe123"
    )
