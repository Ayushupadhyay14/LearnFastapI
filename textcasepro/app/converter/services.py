from sqlalchemy.ext.asyncio import AsyncSession
from app.account.models import User
from app.converter.models import UserCredits, APIKey, CreditRequest
from app.converter.utils import generate_api_key, convert_text
from sqlalchemy import select, delete
from fastapi import HTTPException
from app.converter.schemas import ConvertRequest

async def generate_user_api_key(session: AsyncSession, user: User):
  await session.execute(delete(APIKey).where(APIKey.user_id == user.id))
  new_key = generate_api_key()
  key = APIKey(user_id = user.id, key=new_key)
  session.add(key)
  await session.commit()
  return new_key

async def get_user_api_key(session: AsyncSession, user: User):
  key_obj = await session.scalar(select(APIKey).where(APIKey.user_id == user.id))
  if not key_obj:
    raise HTTPException(status_code=404, detail="API key not found")
  return key_obj.key

async def get_or_create_user_credits(session: AsyncSession, user_id: int):
  credits_obj = await session.scalar(select(UserCredits).where(UserCredits.user_id == user_id))
  if not credits_obj:
    credits_obj = UserCredits(user_id = user_id, credits=10)
    session.add(credits_obj)
    await session.commit()
    await session.refresh(credits_obj)
  return credits_obj

async def get_credit_requests_list(session: AsyncSession, user: User):
  result = await session.scalars(select(CreditRequest).order_by(CreditRequest.created_at.desc()))
  return result.all()

async def submit_credit_request(session: AsyncSession, user: User, credits: int):
  req = CreditRequest(user_id=user.id, credits_requested=credits, status="pending")
  session.add(req)
  await session.commit()
  await session.refresh(req)
  return req

async def approve_credit_request(session: AsyncSession, request_id: int):
  req = await session.get(CreditRequest, request_id)
  if not req:
    raise HTTPException(status_code=404, detail="Request not found")
  if req.status != "pending":
    raise HTTPException(status_code=400, detail="Already processed")
  credits_obj = await get_or_create_user_credits(session, req.user_id)
  credits_obj.credits += req.credits_requested
  req.status = "approved"
  await session.commit()
  await session.refresh(req)
  return req

async def handle_conversion(session: AsyncSession, data: ConvertRequest, user: User):
  credits_obj = await get_or_create_user_credits(session, user.id)
  if credits_obj.credits <= 0:
    raise HTTPException(status_code=402, detail="Out of credits")
  try:
    result = convert_text(data.text, data.operation)
  except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))
  credits_obj.credits -= 1
  await session.commit()
  return result
  
  