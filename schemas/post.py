from typing import Optional

from pydantic import BaseModel
from schemas.user import GetUser
class PostCreate(BaseModel):
    content: str

    class Config:
        orm_mode = True