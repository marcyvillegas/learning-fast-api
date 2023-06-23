from fastapi import FastAPI, APIRouter, Depends, Request, HTTPException, Response
from sqlalchemy.orm import Session, joinedload
from models.post import Post
from models.user import User
from schemas.post import PostCreate
from db import engine, Base
from routers.user import get_db, is_user_logged

app = FastAPI()

Base.metadata.create_all(bind=engine)

post = APIRouter(
    prefix="/post",
    tags=["post"]
)

@post.get("/all")
def get_all_posts(request: Request, db: Session = Depends(get_db)):
    is_user_logged(request)

    posts = db.query(Post).options(joinedload(Post.user)).all()

    return posts

@post.get("/user/{user_id}")
def get_user_post(user_id: int, request: Request, db: Session = Depends(get_db)):
    is_user_logged(request)

    posts = db.query(Post).filter(Post.user_id == user_id).all()
    if not posts:
        raise HTTPException(status_code=404, detail="Posts not found.")

    return posts

@post.get("/{post_id}")
def get_post(post_id: int, request: Request, db: Session = Depends(get_db)):
    is_user_logged(request)

    post = db.query(Post).filter(Post.id == post_id).options(joinedload(Post.user)).first()
    if not post:
        raise HTTPException(status_code=404, detail="Posts not found.")

    return post

@post.post("/{user_id}/add")
def add_post(user_id: int, post: PostCreate, db: Session = Depends(get_db)):

    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    new_post = Post(content=post.content, user=user)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"message": "Completed"}
