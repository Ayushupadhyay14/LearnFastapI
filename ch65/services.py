from sqlmodel import Session, select
from db import engine
from models import User

def create_user(name: str, email:str):
  with Session(engine) as session:
    user = User(name=name, email=email)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
  
def get_all_users():
  with Session(engine) as session:
    stmt = select(User)
    users = session.exec(stmt)
    return users.all()
  
def get_user(user_id: int):
  with Session(engine) as session:
    stmt = select(User).where(User.id == user_id)
    user = session.exec(stmt).first()
    return user

def get_user_with_get(user_id: int):
  with Session(engine) as session:
    user = session.get(User, user_id)
    return user