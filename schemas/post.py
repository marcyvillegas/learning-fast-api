from pydantic import BaseModel
class Post(BaseModel):
    content: str
    user_id: int

    class Config:
        orm_mode = True