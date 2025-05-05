from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.engine import URL
from .config import settings
import logging

logger = logging.getLogger(__name__)

connection_url = settings.DATABASE_URL
engine = create_engine(
    connection_url,
        pool_size=5,               # Set connection pool size
    max_overflow=10,           # Maximum overflow connections
    pool_timeout=30,           # Connection timeout in seconds
    pool_pre_ping=True,        # Enable connection health checks
    pool_recycle=1800,         # Recycle connections after 30 minutes
    connect_args={
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5
    })

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    logger.info("Database tables created/verified successfully")

def get_session():
    with Session(engine) as session:
        yield session
    logger.debug("Creating new database session")

