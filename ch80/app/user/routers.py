from fastapi import APIRouter

router = APIRouter(tags=["users"])

@router.get("/")
async def get_all_users():
  return {"data": "All Users"}

@router.get("/me")
async def get_current_user():
  return {"data": "Current User"}

@router.get("/{user_id}")
async def get_single_user(user_id: int):
  return {"data": "Single User"}