from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserIn(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: int
    password: str


class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: int
    created_date: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    username: EmailStr
    password: str


class TokenData(BaseModel):
    id: Optional[int] = None
