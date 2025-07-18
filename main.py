from fastapi import FastAPI
from db import engine, base
from crud import router as user_router

app = FastAPI()

base.metadata.create_all(bind=engine)

app.include_router(user_router, prefix="/users", tags=["crud operations"])



