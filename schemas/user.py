from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    email: str

class UserLogIn(UserBase):
    email: str
    password: str

class UserCreate(UserBase):
    first_name: str
    last_name: str
    password: str

class GetUser(UserBase):
    first_name: str
    last_name: str

class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]

    class Config:
        orm_mode = True
        exclude = ["password"]