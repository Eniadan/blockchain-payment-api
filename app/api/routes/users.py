from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import (
    create_user as create_user_service,
    get_user as get_user_service,
)


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.post("/", response_model=UserResponse, status_code=201)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    return create_user_service(db, user_data)

@router.get("/{user_id}", response_model=UserResponse)
@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    return get_user_service(db, user_id)