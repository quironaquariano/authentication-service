from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: str
    pawwsord: str


class Token(BaseModel):
    access_token: str
    token_type: str
