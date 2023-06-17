from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    first_name: str
    last_name: str
    password: str

class UserLogIn(UserBase):
    email: str
    password: str

class UserPosts(UserBase):
    post: list

    class Config:
        orm_mode = True