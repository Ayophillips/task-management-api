from sqlmodel import SQLModel, Session, create_engine
from .config import settings
import logging

logger = logging.getLogger(__name__)

engine = create_engine(settings.DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    logger.info("Database tables created successfully")

def get_session():
    with Session(engine) as session:
        yield session
    logger.debug("Creating new database session")

