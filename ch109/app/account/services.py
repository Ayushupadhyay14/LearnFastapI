from app.account.models import User
from sqlalchemy.ext.asyncio import AsyncSession

async def create_user(session: AsyncSession, name: str, email:str):
    user = User(name=name, email=email)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user