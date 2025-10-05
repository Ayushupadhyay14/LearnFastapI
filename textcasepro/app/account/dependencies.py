from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from app.db.config import SessionDep
from app.account.utils import decode_token
from app.account.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/account/login")

async def get_current_user(session: SessionDep, token: str = Depends(oauth2_scheme)) -> User:
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    stmt = select(User).where(User.id == int(payload.get("sub")))
    result = await session.scalars(stmt)
    user = result.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user

async def require_admin(user: User = Depends(get_current_user)) -> User:
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not an Admin")
    return user