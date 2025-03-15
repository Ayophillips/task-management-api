from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.engine import URL
from .config import settings
import logging

logger = logging.getLogger(__name__)

connection_url = f"{settings.DATABASE_URL}?sslmode=require"
engine = create_engine(connection_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    logger.info("Database tables created/verified successfully")

def get_session():
    with Session(engine) as session:
        yield session
    logger.debug("Creating new database session")

