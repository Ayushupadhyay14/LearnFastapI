from db import engine
from tables import users
from sqlalchemy import insert, select, update, delete

# Insert or Create User
async def create_user(name: str, email: str):
  async with engine.connect() as conn:
    stmt = insert(users).values(name=name, email=email)
    await conn.execute(stmt)
    await conn.commit()

# Get Single User by ID
async def get_user_by_id(user_id: int):
   async with engine.connect() as conn:
        stmt = select(users).where(users.c.id == user_id)
        result = await conn.execute(stmt)
        return result.first()
   
# Get All Users
async def get_all_users():
   async with engine.connect() as conn:
        stmt = select(users)
        result = await conn.execute(stmt)
        return result.fetchall()
   
# Update User Email
async def update_user_email(user_id: int, new_email: str):
   async with engine.connect() as conn:
        stmt = update(users).where(users.c.id == user_id).values(email=new_email)
        await conn.execute(stmt)
        await conn.commit()

# Delete User
async def delete_user(user_id: int):
   async with engine.connect() as conn:
        stmt = delete(users).where(users.c.id == user_id)
        await conn.execute(stmt)
        await conn.commit()
