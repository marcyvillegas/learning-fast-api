from fastapi import FastAPI, APIRouter, Depends, Request, Response, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, UserLogIn
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


def is_user_logged(request: Request):
    logged_user = request.cookies.get("logged_user")
    return logged_user is not None


# def create_cookie():


@router.post("/signup")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User is created!"}

@router.post("/login")
def login_user(user: UserLogIn, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user is None:
        raise HTTPException(status_code=400, detail="Email is not registered.")

    validate_password = db.query(User).filter(existing_user.password == user.password).first()
    if validate_password is None:
        raise HTTPException(status_code=400, detail="Incorrect password.")

    # response = Response({"message": "Login successful!"})
    # response.set_cookie(key="logged_user", value=user.email)
    return {"message": "Login successful!"}


