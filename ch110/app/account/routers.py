from fastapi import APIRouter, HTTPException
from app.account.services import (
    create_user, get_user_by_id, get_all_users,
    update_user, delete_user
)

router = APIRouter(prefix="/account", tags=["Account"])

@router.post("/register")
async def register(name: str, email: str):
    return await create_user(name, email)

@router.get("/users")
async def list_users():
    return await get_all_users()

@router.get("/users/{user_id}")
async def get_user(user_id: str):
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}")
async def update_user_route(user_id: str, name: str = None, email: str = None):
    user = await update_user(user_id, name, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/users/{user_id}")
async def delete_user_route(user_id: str):
    success = await delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}


