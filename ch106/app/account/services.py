from app.account.models import User, UserCreate
from sqlmodel import Session, select
from fastapi import HTTPException
from app.account.utils import hash_password, verify_password, create_email_verification_token, verify_token_and_get_user_id, get_user_by_email, create_password_reset_token

def create_user(session: Session, user: UserCreate):
  stmt = select(User).where(User.email == user.email)
  if session.exec(stmt).first():
    raise HTTPException(status_code=400, detail="Email already registered")
  new_user = User(
    email = user.email,
    name = user.name,
    hashed_password= hash_password(user.password),
    is_verified= False
  )
  session.add(new_user)
  session.commit()
  session.refresh(new_user)
  return new_user

def authenticate_user(session: Session, email:str, password: str):
  stmt = select(User).where(User.email == email)
  user = session.exec(stmt).first()
  if not user or not verify_password(password, user.hashed_password):
    return None
  return user

def process_email_verification(user: User):
  token = create_email_verification_token(user.id)
  link = f"http://localhost:8000/account/verify?token={token}"
  print(f"Verify your email: {link}")
  return {"msg": "Verification email sent"}

def verify_email_token(session: Session, token: str):
  user_id = verify_token_and_get_user_id(token, "verify")
  if not user_id:
    raise HTTPException(status_code=400, detail="Invalid or expired token")
  stmt = select(User).where(User.id == user_id)
  user = session.exec(stmt).first()
  if not user:
    raise HTTPException(status_code=404, detail="User not found")
  user.is_verified = True
  session.add(user)
  session.commit()
  return {"msg": "Email verified successfully"}

def change_password(session: Session, user: User, new_password: str):
  user.hashed_password = hash_password(new_password)
  session.add(user)
  session.commit()

def process_password_reset(session: Session, email: str):
  user = get_user_by_email(session, email)
  if not user:
    raise HTTPException(status_code=404, detail="User not found")
  token = create_password_reset_token(user.id)
  link = f"http://localhost:8000/account/reset-password?token={token}"
  print(f"Reset your password: {link}")
  return {"msg": "Password reset link sent"}

def reset_password_with_token(session: Session, token: str, new_password: str):
  user_id = verify_token_and_get_user_id(token, "reset")
  if not user_id:
    raise HTTPException(status_code=400, detail="Invalid or expired token")
  stmt = select(User).where(User.id == user_id)
  user = session.exec(stmt).first()
  if not user:
    raise HTTPException(status_code=404, detail="User not found")
  change_password(session, user, new_password)
  return {"msg": "Password reset successful"}
  