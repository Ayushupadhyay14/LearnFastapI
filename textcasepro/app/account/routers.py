from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.account.models import User
from app.account.schemas import UserCreate, UserOut
from app.db.config import SessionDep
from app.account.utils import create_tokens, verify_refresh_token, revoke_refresh_token
from app.account.dependencies import get_current_user, require_admin
from app.account.services import (
    create_user,
    authenticate_user,
    process_email_verification,
    verify_email_token,
    change_password,
    process_password_reset,
    reset_password_with_token,
)

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register(session: SessionDep, user: UserCreate):
    return await create_user(session, user)

@router.post("/login")
async def login(session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    tokens = await create_tokens(session, user)
    response = JSONResponse(content={"access_token": tokens["access_token"]})
    response.set_cookie(
        "refresh_token",
        tokens["refresh_token"],
        httponly=True,
        secure=True,
        samesite="Lax",
        max_age=60 * 60 * 24 * 7
    )
    return response

@router.post("/refresh")
async def refresh_token(session: SessionDep, request: Request):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="Missing refresh token")
    
    user = await verify_refresh_token(session, token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    
    return await create_tokens(session, user)

@router.get("/me", response_model=UserOut)
async def me(user: User = Depends(get_current_user)):
    return user

@router.post("/verify-request")
async def send_verification_email(user: User = Depends(get_current_user)):
    return process_email_verification(user)

@router.get("/verify")
async def verify_email(session: SessionDep, token: str):
    return await verify_email_token(session, token)

@router.post("/change-password")
async def password_change(session: SessionDep, new_password: str, user: User = Depends(get_current_user)):
    await change_password(session, user, new_password)
    return {"msg": "Password changed successfully"}

@router.post("/forgot-password")
async def forgot_password(session: SessionDep, email: str):
    return await process_password_reset(session, email)

@router.post("/reset-password")
async def reset_password(session: SessionDep, token: str, new_password: str):
    return await reset_password_with_token(session, token, new_password)

@router.get("/admin")
async def admin(user: User = Depends(require_admin)):
    return {"msg": f"Welcome Admin {user.name}"}

@router.post("/logout")
async def logout(session: SessionDep, request: Request):
    token = request.cookies.get("refresh_token")
    if token:
        await revoke_refresh_token(session, token)
    response = JSONResponse(content={"detail": "Logged out"})
    response.delete_cookie("refresh_token")
    return response