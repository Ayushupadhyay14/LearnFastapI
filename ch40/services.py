from db import engine
from tables import users, posts
from sqlalchemy import insert, select

# Insert or Create User
def create_user(name: str, email: str):
  with engine.connect() as conn:
    stmt = insert(users).values(name=name, email=email)
    conn.execute(stmt)
    conn.commit()

# Insert or Create Post
def create_post(user_id: int, title: str, content: str):
    with engine.connect() as conn:
        stmt = insert(posts).values(user_id=user_id, title=title, content=content)
        conn.execute(stmt)
        conn.commit()

# Join Users and Posts (List all posts with author names)
def get_posts_with_author():
    with engine.connect() as conn:
        stmt = select(
           posts.c.id,
           posts.c.title,
           users.c.name.label("author_name")
        ).join(users, posts.c.user_id == users.c.id)
        result = conn.execute(stmt).fetchall()
        return result