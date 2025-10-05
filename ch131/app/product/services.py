from app.core.log_config import logger

async def get_all_products():
  logger.error("Data could not fetch due to Db int issue")
  return {"msg": "All Products"}

async def create_product():
  return {"msg": "Create Products"}
