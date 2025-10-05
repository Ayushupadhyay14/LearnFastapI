from fastapi import APIRouter

router = APIRouter()

@router.get("/products")
async def get_all_products():
  return {"data": "All Products"}

@router.get("/products/{product_id}")
async def get_single_product(product_id: int):
  return {"data": "Single Product"}