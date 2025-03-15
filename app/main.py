import logging
from app.core.logging import setup_logging
from fastapi import FastAPI, Depends, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.exceptions import RequestValidationError, HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlmodel import Session, select

from app.database import create_db_and_tables, get_session
from app.api import auth, tasks
from app.config import settings
from app.core.errors import ErrorHandlers
from contextlib import asynccontextmanager

logger = setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up application")
    try:
        create_db_and_tables()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {str(e)}")
        # Don't raise the exception - allow app to start even if tables exist
    yield
    logger.info("Shutting down application")

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(tasks.router)

# Register error handlers
app.add_exception_handler(RequestValidationError, ErrorHandlers.validation_error_handler)
app.add_exception_handler(IntegrityError, ErrorHandlers.integrity_error_handler)
app.add_exception_handler(Exception, ErrorHandlers.global_exception_handler)
app.add_exception_handler(HTTPException, ErrorHandlers.http_exception_handler)
app.add_exception_handler(SQLAlchemyError, ErrorHandlers.sqlalchemy_error_handler)

# Custom OpenAPI schema to improve documentation
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        description="A Task Management API with authentication, CRUD operations, and database integration.",
        routes=app.routes,
    )
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/")
def read_root():
    return {"message": "Welcome to the Task Management API", "version": settings.PROJECT_VERSION}

@app.get("/health", tags=["Health"], status_code=status.HTTP_200_OK)
async def health_check(session: Session = Depends(get_session)):
    """
    Check the health of the application and its dependencies.
    Returns:
        dict: Health check results including database status and app version
    """
    health_status = {
        "status": "healthy",
        "version": settings.PROJECT_VERSION,
        "database": {
            "status": "healthy",
            "error": None
        }
    }

    try:
        # Test database connection
        session.exec(select(1)).first()
    except Exception as e:
        error_message = str(e)
        logger.error(f"Database health check failed: {error_message}")
        health_status.update({
            "status": "unhealthy",
            "database": {
                "status": "unhealthy",
                "error": error_message
            }
        })
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=health_status
        )

    return health_status

if __name__ == "__main__":
    import uvicorn # type: ignore
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

