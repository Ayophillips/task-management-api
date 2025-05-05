import logging
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from app.config import settings
from app.schemas.user import TokenData
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from app.models.user import User
from app.database import get_session

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    result = pwd_context.verify(plain_password, hashed_password)
    if not result:
        logger.warning("Failed password verification attempt")
    return result

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            logger.warning("Token payload missing username")
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        logger.warning("Invalid JWT token")
        raise credentials_exception
    
    # user = await User.find_one({"username": token_data.username})
    user = session.exec(select(User).where(User.username == token_data.username)).first()
    if user is None:
        logger.warning(f"User not found: {token_data.username}")
        raise credentials_exception
    if not user.is_active:
        logger.warning(f"Inactive user attempted login: {user.username}")
        raise HTTPException(status_code=400, detail="Inactive user")
    logger.info(f"Successfully authenticated user: {user.username}")
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        logger.warning(f"Inactive user attempt to access: {current_user.username}")
        raise HTTPException(status_code=403, detail="Inactive user, Account is deactivated")
    return current_user
