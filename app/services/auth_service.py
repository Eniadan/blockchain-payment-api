from fastapi import HTTPException
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.models.user import User


password_hash = PasswordHash.recommended()


# Retrieve a user by email so their stored credentials can be verified.
def get_user_by_email(
    db: Session,
    email: str,
):
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


# Compare the supplied password with the password hash stored for the user.
def verify_password(
    password: str,
    password_hash_value: str,
):
    return password_hash.verify(
        password,
        password_hash_value,
    )


# Authenticate the user's credentials and issue an access token.
def authenticate_user(
    db: Session,
    email: str,
    password: str,
):
    user = get_user_by_email(db, email)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    access_token = create_access_token(user.id)

    return user, access_token