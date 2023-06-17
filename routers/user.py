from fastapi import FastAPI, APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import update
from models.user import User
from schemas.user import UserCreate, UserLogIn, GetUser, UserUpdate
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

# CREATE
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

# READ ALL
@router.get("/all-users")
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# READ ONE
@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.id == user_id).first()
    if existing_user is None:
        raise HTTPException(status_code=400, detail="Email is not registered.")
    return existing_user

# EDIT
@router.put("/edit/{user_id}")
def edit_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
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
@router.delete("delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.id == user_id).first()
    if existing_user is None:
        raise HTTPException(status_code=400, detail="No existing user.")

    db.delete(existing_user)
    db.commit()
    return {"message": "Successfully deleted user!"}
