from fastapi import FastAPI
from app.user import services as user_services
from pydantic import BaseModel

app = FastAPI()

class UserCreate(BaseModel):
  name: str
  email: str

@app.post("/user")
async def user_create(user: UserCreate):
  await user_services.create_user(name=user.name, email=user.email)
  return {"status":"created"}

@app.get("/users")
async def all_users():
  users = await user_services.get_all_users()
  return users


