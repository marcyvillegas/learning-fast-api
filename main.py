from fastapi import FastAPI
from routers.user import router

app = FastAPI(debug=True)

app.include_router(router, prefix="/api")