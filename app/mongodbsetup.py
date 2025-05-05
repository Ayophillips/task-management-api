from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.config import settings
from app.models.user import User
from app.models.task import Task
import logging

logger = logging.getLogger(__name__)

async def init_mongodb():
    """Initialize MongoDB connection and Beanie ODM"""
    try:
        # Create Motor client
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        
        # Initialize Beanie with the document models
        await init_beanie(
            database=client[settings.MONGODB_DB_NAME],
            document_models=[User, Task]
        )
        
        logger.info("Successfully connected to MongoDB")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {str(e)}")
        raise

async def close_mongodb_connection():
    """Close MongoDB connection"""
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    client.close()
    logger.info("MongoDB connection closed")