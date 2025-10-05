from fastapi import APIRouter

router = APIRouter()

@router.get("/users", tags=["users"])
async def get_all_users():
  return {"data": "All Users"}

@router.get("/users/me", tags=["users"])
async def get_current_user():
  return {"data": "Current User"}

@router.get("/users/{user_id}", tags=["custom"])
async def get_single_user(user_id: int):
  return {"data": "Single User"}

# router = APIRouter(tags=["users"])

# @router.get("/users")
# async def get_all_users():
#   return {"data": "All Users"}

# @router.get("/users/me")
# async def get_current_user():
#   return {"data": "Current User"}

# @router.get("/users/{user_id}", tags=["custom"])
# async def get_single_user(user_id: int):
#   return {"data": "Single User"}