from models import create_tables, drop_tables
import asyncio
from services import *

async def main():
  # Create Tables
  # await create_tables()

  # Create Data
  # await create_user("sonam", "sonam@example.com")
  # await create_user("raj", "raj@example.com")

  # Read data
  # print(await get_user_by_id(1))
  # print(await get_all_users())

  # Update data
  # await update_user_email(1, "sonam@newdomain.com")

  # Delete Data
  await delete_user(2)

asyncio.run(main())