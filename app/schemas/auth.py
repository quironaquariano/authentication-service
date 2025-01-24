from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class ResetPassword(BaseModel):
    new_password: str
    token: str
