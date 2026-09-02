from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.api.routes.users import router as users_router

app = FastAPI(
    title="Blockchain Payment API",
    version="1.0.0",
)

app.include_router(users_router)


@app.get("/")
def root():
    return {
        "message": "Blockchain Payment API is running"
    }
@app.get("/db-test")
def db_test():
    return {"message": "Database connection is working"}

