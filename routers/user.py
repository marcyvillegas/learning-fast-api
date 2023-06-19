from fastapi import FastAPI, APIRouter, Depends, Request, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import update
from models.user import User
from schemas.user import UserCreate, UserLogIn, UserUpdate
from db import sessionLocal, engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

user = APIRouter(
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
    if logged_user is None:
        raise HTTPException(status_code=400, detail="User is not logged in.")

def create_cookie(response: Response, user: str):
    response.set_cookie(key="logged_user", value=user)

# CREATE
@user.post("/signup")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User is created!"}

@user.post("/login")
def login_user(user: UserLogIn, response: Response, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user is None:
        raise HTTPException(status_code=400, detail="Email is not registered.")

    validate_password = db.query(User).filter(existing_user.password == user.password).first()
    if validate_password is None:
        raise HTTPException(status_code=400, detail="Incorrect password.")

    create_cookie(response, existing_user.id)

    return {"message": "Login successful!"}

@user.get("/logout")
def logout_user(response: Response):
    response.delete_cookie("logged_user")
    return {"message": "Log out successfully!"}

# READ ALL
@user.get("/all-users")
def get_all_users(request: Request, db: Session = Depends(get_db)):
    is_user_logged(request)

    users = db.query(User).all()
    return users

# READ ONE
@user.get("/{user_id}")
def get_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    is_user_logged(request)

    existing_user = db.query(User).filter(User.id == user_id).first()
    if existing_user is None:
        raise HTTPException(status_code=400, detail="Email is not registered.")
    return existing_user

# EDIT
@user.put("/edit/{user_id}")
def edit_user(user_id: int, user: UserUpdate, request: Request, db: Session = Depends(get_db)):
    is_user_logged(request)

    existing_user = db.query(User).filter(User.id == user_id).first()
    if existing_user is None:
        raise HTTPException(status_code=400, detail="Email is not registered.")

    update_user = user.dict(exclude_unset=True)
    if update_user:
        statement = update(User).where(User.id == user_id).values(**update_user)
        db.execute(statement)
        db.commit()
    return {"message": "Successfully updated the user!"}

# DELETE
@user.delete("/delete/{user_id}")
def delete_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    is_user_logged(request)

    existing_user = db.query(User).filter(User.id == user_id).first()
    if existing_user is None:
        raise HTTPException(status_code=400, detail="No existing user.")

    db.delete(existing_user)
    db.commit()
    return {"message": "Successfully deleted user!"}
