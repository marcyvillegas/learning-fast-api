from fastapi import FastAPI, APIRouter, Depends, Request, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import update
from models.user import User
from schemas.user import UserCreate, UserLogIn, UserUpdate
from db import sessionLocal, engine, Base
from redis import asyncio as aioredis

app = FastAPI()

Base.metadata.create_all(bind=engine)

user = APIRouter(
    prefix="/user",
    tags=["user"]
)

redis = aioredis.from_url("redis://localhost")
TTL = 20 # seconds expiration

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

async def user_authentication():
    logged_user = await redis.get("logged_user")
    if logged_user is None:
        raise HTTPException(status_code=400, detail="User is not logged in.")

async def create_redis_key(user: str):
    await redis.set("logged_user", user)
    await redis.expire("logged_user", TTL)

# Trying redis
@user.get("/trying-redis")
async def create_cache():
    await redis.set("my-key", "value")
    value = await redis.get("my-key")
    print(value)
    return {"cache": value}

# CREATE
@user.post("/signup")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User is created!"}

@user.post("/login")
async def login_user(user: UserLogIn, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user is None:
        raise HTTPException(status_code=400, detail="Email is not registered.")

    validate_password = db.query(User).filter(existing_user.password == user.password).first()
    if validate_password is None:
        raise HTTPException(status_code=400, detail="Incorrect password.")

    await create_redis_key(existing_user.id)

    return {"message": "Login successful!"}

@user.get("/logout")
async def logout_user():
    await redis.delete("logged_user")
    return {"message": "Log out successfully!"}

# READ ALL
@user.get("/all-users")
async def get_all_users(db: Session = Depends(get_db)):
    await user_authentication()

    users = db.query(User).all()
    return users

# READ ONE
@user.get("/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    await user_authentication()

    existing_user = db.query(User).filter(User.id == user_id).first()
    if existing_user is None:
        raise HTTPException(status_code=400, detail="Email is not registered.")
    return existing_user

# EDIT
@user.put("/edit/{user_id}")
async def edit_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    await user_authentication()

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
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    await user_authentication()

    existing_user = db.query(User).filter(User.id == user_id).first()
    if existing_user is None:
        raise HTTPException(status_code=400, detail="No existing user.")

    db.delete(existing_user)
    db.commit()
    return {"message": "Successfully deleted user!"}
