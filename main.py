from fastapi import FastAPI
from routers.user import user
from routers.post import post

app = FastAPI(debug=True)

app.include_router(user, prefix="/api")
app.include_router(post, prefix="/api")