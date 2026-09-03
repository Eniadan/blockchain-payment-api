from fastapi import HTTPException
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate


password_hash = PasswordHash.recommended()
def create_user(
    db: Session,
    user_data: UserCreate,
):
    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="User with this email already exists",
        )
    hashed_password = password_hash.hash(user_data.password)
    user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        password_hash=hashed_password,
    )


    db.add(user)
    db.commit()
    db.refresh(user)

    return user
def get_user(
    db: Session,
    user_id: int,
):
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user