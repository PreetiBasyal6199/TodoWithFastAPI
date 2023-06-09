from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserPostSchema(BaseModel):
    email: EmailStr = Field(...)
    full_name: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "user": {
                "email": "john@gmail.com",
                "full_name": "John",
                "password": "Hello"
            }
        }


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "user_login": {
                "email": "john@gmail.com",
                "password": "Hello"
            }
        }


class TodoPostSchema(BaseModel):
    title: str = Field(...)
    is_completed: bool = Field(default=False)


class TodoUpdateSchema(BaseModel):
    title: Optional[str]
    is_completed: Optional[bool]
