from fastapi import APIRouter, Depends, HTTPException, Request
from app.account.services import create_user, authenticate_user, process_email_verification, verify_email_token, change_password, process_password_reset, reset_password_with_token
from app.account.models import UserCreate, UserOut
from app.db.config import SessionDep
from fastapi.security import OAuth2PasswordRequestForm
from app.account.utils import create_tokens, verify_refresh_token, revoke_refresh_token
from fastapi.responses import JSONResponse
from app.account.dependencies import get_current_user, require_admin

router = APIRouter(prefix="/account", tags=["Account"])

@router.post("/register", response_model=UserOut)
def register(session: SessionDep, user: UserCreate):
  return create_user(session, user)

@router.post("/login")
def login(session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()):
  user = authenticate_user(session, form_data.username, form_data.password)
  if not user:
    raise HTTPException(status_code=401, detail="Invalid credentials")
  tokens = create_tokens(session, user)
  response = JSONResponse(content={"access_token": tokens["access_token"]})
  response.set_cookie("refresh_token", tokens["refresh_token"], httponly=True, secure=True, samesite="Lax", max_age=60 * 60 * 24 * 7)
  return response

@router.post("/refresh")
def refresh_token(session: SessionDep, request: Request):
  token = request.cookies.get("refresh_token")
  if not token:
    raise HTTPException(status_code=401, detail="Missing refresh token")
  user = verify_refresh_token(session, token)
  if not user:
    raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
  return create_tokens(session, user)

@router.get("/me", response_model=UserOut)
def me(user = Depends(get_current_user)):
  return user

@router.post("/verify-request")
def send_verfication_email(user = Depends(get_current_user)):
  return process_email_verification(user)
  
@router.get("/verify")
def verify_email(session: SessionDep, token: str):
  return verify_email_token(session, token)

@router.post("/change-password")
def password_change(session: SessionDep, new_password: str, user = Depends(get_current_user)):
  change_password(session, user, new_password)
  return {"msg": "Password changed successfully"}

@router.post("/forgot-password")
def forgot_password(session: SessionDep, email: str):
  return process_password_reset(session, email)

@router.post("/reset-password")
def reset_password(session: SessionDep, token: str, new_password: str):
    return reset_password_with_token(session, token, new_password)

@router.get("/admin")
def admin(user = Depends(require_admin)):
  return {"msg": f"Welcome Admin {user.name}"}

@router.post("/logout")
def logout(session: SessionDep, request: Request):
  token = request.cookies.get("refresh_token")
  if token:
    revoke_refresh_token(session, token)
  response = JSONResponse(content={"detail": "Logged out"})
  response.delete_cookie("refresh_token")
  return response