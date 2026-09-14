from pydantic import BaseModel, EmailStr


# This is the data we need when a user logs in.
class LoginRequest(BaseModel):
    email: EmailStr
    password: str