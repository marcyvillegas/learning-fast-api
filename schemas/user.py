from pydantic import BaseModel

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str

class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True