from fastapi import Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.config import SessionDep
from app.account.models import User
from app.converter.models import APIKey

async def get_user_from_api_key(
    session: SessionDep,
    x_api_key: str = Header(..., alias="X-API-KEY")
):
  key_obj = await session.scalar(select(APIKey).where(APIKey.key == x_api_key))
  if not key_obj:
    raise HTTPException(status_code=401, detail="Invalid API key")
  return await session.get(User, key_obj.user_id)