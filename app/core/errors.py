from fastapi import Request, status
from fastapi.exceptions import RequestValidationError, HTTPException
import logging
import traceback
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import Union, Dict, Any

# Configure logger
logger = logging.getLogger(__name__)

class ErrorHandlers:
    @staticmethod
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        error_location = f"{request.method} {request.url.path}"
        logger.error(f"Database integrity error at {error_location}: {str(exc)}")
        logger.debug(f"Integrity error details: {traceback.format_exc()}")
        
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Database integrity error occurred. Possibly a duplicate entry."},
        )

    @staticmethod
    async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
        # Handle other database-related errors
        error_location = f"{request.method} {request.url.path}"
        logger.error(f"Database error at {error_location}: {str(exc)}")
        logger.debug(f"Database error details: {traceback.format_exc()}")
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "A database error occurred. Please try again later."},
        )
    
    @staticmethod
    async def validation_error_handler(request: Request, exc: RequestValidationError):
        error_location = f"{request.method} {request.url.path}"
        logger.error(f"Validation error at {error_location}: {str(exc)}")
        
        error_details = []
        for error in exc.errors():
            error_details.append({
                "loc": error.get("loc", []),
                "msg": error.get("msg", ""),
                "type": error.get("type", "")
            })
            
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": "Validation error",
                "errors": error_details
            },
        )

    @staticmethod
    async def http_exception_handler(request: Request, exc: HTTPException):
        error_location = f"{request.method} {request.url.path}"
        logger.warning(f"HTTP exception at {error_location}: {exc.status_code} - {exc.detail}")
        
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=getattr(exc, "headers", None)
        )

    @staticmethod
    async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """
        Global exception handler for all uncaught exceptions.
        Logs the error details but returns a generic error message to the client.
        """
        error_location = f"{request.method} {request.url.path}"
        
        import uuid
        error_id = str(uuid.uuid4())
        
        logger.critical(
            f"Uncaught exception at {error_location} [Error ID: {error_id}]: {str(exc)}"
        )
        logger.error(f"Request details: {request.client.host} - {request.headers.get('user-agent', 'Unknown')}")
        logger.debug(f"Exception traceback: {traceback.format_exc()}")
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "An unexpected error occurred.",
                "error_id": error_id
            }
        )
