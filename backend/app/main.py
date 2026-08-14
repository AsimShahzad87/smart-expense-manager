from fastapi import FastAPI
from sqlalchemy import text

from app.core.config import settings
from app.database.connection import engine

from app.api.v1.auth import router as auth_router
from app.api.v1.accounts import router as accounts_router


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend API for Smart Expense Manager",
)


app.include_router(
    auth_router,
    prefix="/api/v1",
)


app.include_router(
    accounts_router,
    prefix="/api/v1",
)


@app.get("/")
def root():
    return {
        "message": "Smart Expense Manager API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "UP"
    }


@app.get("/health/database")
def database_health():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "status": "UP",
        "database": "CONNECTED"
    }