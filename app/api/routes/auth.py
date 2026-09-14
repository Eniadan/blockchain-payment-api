from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import LoginRequest
from app.services.auth_service import authenticate_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# Authenticate the user and return the authenticated user's details.
# Credential validation is delegated to the service layer so the route
# remains responsible only for handling the HTTP request and response.
@router.post("/login")
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db=db,
        email=login_data.email,
        password=login_data.password,
    )

    return {
        "message": "Login successful",
        "user_id": user.id,
        "email": user.email,
    }