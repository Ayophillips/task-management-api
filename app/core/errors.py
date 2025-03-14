from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

class ErrorHandlers:
    @staticmethod
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        return JSONResponse(
            status_code=400,
            content={"detail": "Database integrity error occurred. Possibly a duplicate entry."},
        )

