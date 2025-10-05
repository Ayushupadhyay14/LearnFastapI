from app.db.config import SessionLocal
from app.user.models import User
from sqlalchemy import select

# Insert or Create User
def create_user(name: str, email: str):
  with SessionLocal() as session:
    user = User(name=name, email=email)
    session.add(user)
    session.commit()

# Read All User
def get_all_users():
  with SessionLocal() as session:
    stmt = select(User)
    users = session.scalars(stmt)
    return users.all()