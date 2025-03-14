from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from sqlalchemy.exc import IntegrityError

from app.database import create_db_and_tables
from app.api import auth, tasks
from app.config import settings
from app.core.errors import ErrorHandlers
from contextlib import asynccontextmanager

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(tasks.router)

app.add_exception_handler(IntegrityError, ErrorHandlers.integrity_error_handler)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

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

if __name__ == "__main__":
    import uvicorn # type: ignore
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

