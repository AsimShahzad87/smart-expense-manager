from fastapi import FastAPI

app = FastAPI(
    title="Smart Expense Manager API",
    version="0.1.0",
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