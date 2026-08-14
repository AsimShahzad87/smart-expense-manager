from fastapi import FastAPI
from sqlalchemy import text

from app.core.config import settings
from app.database.connection import engine


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend API for Smart Expense Manager",
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