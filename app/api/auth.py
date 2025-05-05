from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from sqlmodel import Session, select
import logging

from app.database import get_session
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, Token
from app.core.security import verify_password, get_password_hash, create_access_token, get_current_active_user, get_current_user
from app.config import settings
from typing import Set

logger = logging.getLogger(__name__)

# In-memory token blacklist
# In production, this will be replaced with a Redis or database solution
BLACKLISTED_TOKENS: Set[str] = set()

router = APIRouter(tags=["Authentication"])

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, session: Session = Depends(get_session)):
    # Check if user with this email or username already exists

    # existing_user = await User.find_one({
    #     "$or": [
    #         {"email": user.email},
    #         {"username": user.username}
    #     ]
    # })
    
    # if existing_user:
    #     if existing_user.email == user.email:
    #         logger.warning(f"Registration attempt with existing email: {user.email}")
    #         raise HTTPException(status_code=400, detail="Email already registered")
    #     else:
    #         raise HTTPException(status_code=400, detail="Username already registered")
    

    db_user = session.exec(select(User).where(User.email == user.email)).first()
    if db_user:
        logger.warning(f"Registration attempt with existing email: {user.email}")
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = session.exec(select(User).where(User.username == user.username)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    # await db_user.insert()
    
    logger.info(f"Successfully registered new user: {user.username}")
    return db_user

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    # Check if user exists
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        logger.warning(f"Failed login attempt for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    logger.info(f"Successful login for user: {form_data.username}")
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(token: str = Depends(get_current_user)):
    """
    Logout endpoint that invalidates the current token by adding it to a blacklist
    """
    # Add token to blacklist
    BLACKLISTED_TOKENS.add(token)
    logger.info(f"Token successfully blacklisted")
    return {"detail": "Successfully logged out"}
