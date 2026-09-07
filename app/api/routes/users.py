from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.user import UserCreate, UserResponse

from app.services.user_service import (
    create_user as create_user_service,
    get_user as get_user_service,
)

# Create a router for all user-related API endpoints.
# The prefix and tags keep user routes organized in the API documentation.
router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

# Create a new user through the user registration endpoint.
# UserCreate validates the incoming request data before it reaches the service.
# UserResponse controls which user fields are returned to the client.
@router.post("/", response_model=UserResponse, status_code=201)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    # Pass the validated request data and database session
    # to the service layer where the registration business logic lives.
    return create_user_service(db, user_data)


# Retrieve a user by their unique database ID.
# UserResponse prevents sensitive database fields such as password_hash
# from being exposed in the API response.
@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    # Delegate the user lookup to the service layer.
    return get_user_service(db, user_id)