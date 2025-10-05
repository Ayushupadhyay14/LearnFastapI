from fastapi import FastAPI
from app.db.config import create_tables
from contextlib import asynccontextmanager
from app.user.services import *

@asynccontextmanager
async def lifespan(app: FastAPI):
  create_tables()
  yield

app = FastAPI(lifespan=lifespan)

@app.post("/user")
def user_create(new_user: dict):
  user = create_user(name=new_user["name"], email=new_user["email"])
  return user

@app.get("/users")
def all_users():
  users = get_all_users()
  return users