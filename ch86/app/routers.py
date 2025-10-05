from fastapi import Depends, Header, HTTPException, APIRouter
from typing import Annotated

async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "my-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

# router = APIRouter(dependencies=[Depends(verify_token)])
router = APIRouter()

@router.get("/items")
async def read_items():
    return {"data": "All Items"}