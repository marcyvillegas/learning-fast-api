from fastapi import APIRouter, Depends
from fastapi import FastAPI
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, UserBase
from db import sessionLocal, engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/add", response_model=UserBase)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return user.dict()
