from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
from jose import jwt, JWTError
from sqlmodel import Session, select
import uuid
from app.account.models import RefreshToken, User

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
  return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
  return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
  to_encode = data.copy()
  expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
  to_encode.update({"exp": expire})
  return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_tokens(session: Session, user: User):
  access_token = create_access_token(data={"sub": str(user.id)})
  refresh_token_str = str(uuid.uuid4())
  expires_at = datetime.now(timezone.utc) + timedelta(days=7)
  refresh_token = RefreshToken(
    user_id = user.id,
    token = refresh_token_str,
    expires_at= expires_at
  )
  session.add(refresh_token)
  session.commit()
  return {
    "access_token": access_token,
    "refresh_token": refresh_token_str,
    "token_type": "bearer"
  }

def verify_refresh_token(session: Session, token: str):
  stmt = select(RefreshToken).where(RefreshToken.token == token)
  db_token = session.exec(stmt).first()
  if db_token and not db_token.revoked:
    expires_at = db_token.expires_at
    if expires_at.tzinfo is None:
      expires_at = expires_at.replace(tzinfo=timezone.utc)
    if expires_at > datetime.now(timezone.utc):
      stmt = select(User).where(User.id == db_token.user_id)
      return session.exec(stmt).first()
  return None

def decode_token(token: str):
  try:
    return jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
  except JWTError:
    return None
  
def create_email_verification_token(user_id: int):
  expire = datetime.now(timezone.utc) + timedelta(hours=1)
  to_encode = {"sub": str(user_id), "type": "verify", "exp": expire}
  return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token_and_get_user_id(token: str, token_type: str):
  payload = decode_token(token)
  if not payload or payload.get("type") != token_type:
    return None
  return int(payload.get("sub"))

def get_user_by_email(session: Session, email: str):
  stmt = select(User).where(User.email == email)
  return session.exec(stmt).first()

def create_password_reset_token(user_id: int):
  expire = datetime.now(timezone.utc) + timedelta(hours=1)
  to_encode = {"sub": str(user_id), "type": "reset", "exp": expire}
  return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def revoke_refresh_token(session: Session, token: str):
  stmt = select(RefreshToken).where(RefreshToken.token == token)
  db_token = session.exec(stmt).first()
  if db_token:
    db_token.revoked = True
    session.commit()

