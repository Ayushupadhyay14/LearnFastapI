from models import User, Post
from db import SessionLocal
from sqlalchemy import select, asc

# Insert or Create user
def create_user(name: str, email:str):
  with SessionLocal() as session:
    user = User(name=name, email=email)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# Insert or Create Post
def create_post(user_id: int, title: str, content:str):
  with SessionLocal() as session:
    post = Post(user_id=user_id, title=title, content=content)
    session.add(post)
    session.commit()

# Read user by ID
def get_user_by_id(user_id: int):
    with SessionLocal() as session:
      user = session.get_one(User, user_id)
      return user

# Read post by ID
def get_post_by_id(post_id: int):
    with SessionLocal() as session:
      stmt = select(Post).where(Post.id == post_id)
      post = session.scalars(stmt).one()
      return post
    
# Read All user
def get_all_users():
    with SessionLocal() as session:
       stmt = select(User)
       users = session.scalars(stmt).all()
       return users
    
# Read all posts for an user
def get_posts_by_user(user_id: int):
    with SessionLocal() as session:
       user = session.get(User, user_id)
       posts = user.posts if user else []
       return posts
    
# Update user email
def update_user_email(user_id: int, new_email: str):
    with SessionLocal() as session:
       user = session.get(User, user_id)
       if user:
          user.email = new_email
          session.commit()
       return user
    
# Delete Post
def delete_post(post_id: int):
    with SessionLocal() as session:
       post = session.get(Post, post_id)
       if post:
          session.delete(post)
          session.commit()

# Order by
def get_users_ordered_by_name():
    with SessionLocal() as session:
       stmt = select(User).order_by(asc(User.name))
       users = session.scalars(stmt).all()
       return users