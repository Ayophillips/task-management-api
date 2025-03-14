from fastapi import Depends
from app.core.security import get_current_active_user
from app.database import get_session
from sqlmodel import Session

def get_current_user_dependency():
    return Depends(get_current_active_user)

def get_db_session():
    return Depends(get_session)

