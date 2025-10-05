from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlmodel import select
from app.db.config import SessionDep
from app.account.utils import decode_token
from app.account.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="account/login")

def get_current_user(session: SessionDep, token: str = Depends(oauth2_scheme)):
  payload = decode_token(token)
  if not payload:
    raise HTTPException(status_code=401, detail="Invalid credentials")
  stmt = select(User).where(User.id == int(payload.get("sub")))
  user = session.exec(stmt).first()
  if not user:
    raise HTTPException(status_code=404, detail="User not found")
  return user

def require_admin(user: User = Depends(get_current_user)):
  if not user.is_admin:
     raise HTTPException(status_code=403, detail="You are not an Admin")
  return user