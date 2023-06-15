from enum import Enum
from pydantic import BaseModel, EmailStr


# -- PREDEFINED VALUES IN MODEL --
class Books(str, Enum):
    book1 = "book1"
    book2 = "book2"
    book3 = "book3"


# -- REQUEST BODY --
# data sent from client
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None

# -- REDUCE DUPLICATION --
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str
