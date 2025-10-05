from fastapi import APIRouter, Depends
from app.converter.schemas import APIKeyOut, CreditBalance, CreditRequestOut, CreditRequestCreate, ConvertResponse, ConvertRequest
from app.db.config import SessionDep
from app.account.models import User
from typing import List
from app.converter.deps import get_user_from_api_key
from app.account.dependencies import get_current_user, require_admin
from app.converter.services import generate_user_api_key, get_user_api_key, get_or_create_user_credits, get_credit_requests_list, submit_credit_request, approve_credit_request, handle_conversion

router = APIRouter()

@router.post("/generate-api-key", response_model=APIKeyOut)
async def generate_api_key_view(
    session: SessionDep,
    user: User = Depends(get_current_user)
):
  key = await generate_user_api_key(session, user)
  return {"key": key}

@router.get("/me/api-key", response_model=APIKeyOut)
async def get_my_api_key(
    session: SessionDep,
    user: User = Depends(get_current_user),
):
  key = await get_user_api_key(session, user)
  return {"key": key}

@router.get("/me/credits", response_model=CreditBalance)
async def get_my_credits(
    session: SessionDep,
    user: User = Depends(get_current_user)
):
  credits_obj = await get_or_create_user_credits(session, user.id)
  return {"credits": credits_obj.credits}

@router.get("/credit-requests", response_model=List[CreditRequestOut])
async def list_requests(
    session: SessionDep,
    user: User = Depends(require_admin)
):
  return await get_credit_requests_list(session, user)

@router.post("/buy-credits", response_model=CreditRequestOut)
async def buy_credits(
    session: SessionDep,
    data: CreditRequestCreate,
    user: User = Depends(get_current_user),
):
  req = await submit_credit_request(session, user, data.credits_requested)
  return req

@router.post("/approve-credit/{request_id}", response_model=CreditRequestOut)
async def approve_request(
    session: SessionDep,
    request_id: int,
    user: User = Depends(require_admin),
):
  return await approve_credit_request(session, request_id)

@router.post("/convert", response_model=ConvertResponse)
async def convert( session: SessionDep,
    data: ConvertRequest,
    user: User = Depends(get_user_from_api_key),
):
  result = await handle_conversion(session, data, user)
  return {"result": result}