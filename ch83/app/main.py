from fastapi import FastAPI, Depends
from typing import Annotated

app = FastAPI()

# Hierarchical Dependencies
async def user_auth():
  return {"user_id": "123"}

async def user_role(user: Annotated[dict, Depends(user_auth)]):
  return {"user_id": user["user_id"], "role": "admin"}

@app.get("/admin")
async def admin_only(role: Annotated[dict, Depends(user_role)]):
  return role

