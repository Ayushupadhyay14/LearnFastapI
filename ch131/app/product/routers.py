from fastapi import APIRouter
from app.product.services import get_all_products, create_product
from app.core.log_config import logger

router = APIRouter()

@router.get("")
async def list_all_products():
  logger.info("Product all products route accessed")
  return await get_all_products()

@router.get("create")
async def product_create():
  return await create_product()
