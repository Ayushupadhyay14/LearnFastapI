from sqlmodel import Session, select
from app.db.config import engine
from app.user.models import User

def create_user(name: str, email: str):
  user = User(name=name, email=email)
  with Session(engine) as session:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
  
def get_all_users():
  with Session(engine) as session:
    stmt = select(User)
    users = session.exec(stmt)
    return users.all()