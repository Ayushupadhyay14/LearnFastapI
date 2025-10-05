from fastapi import APIRouter
from app.db.config import SessionDep
from app.product.schemas import ProductBase, ProductRead
from app.product.services import create_product

router = APIRouter(prefix="/products", tags=["Product"])

@router.post("/create", response_model=ProductRead)
async def product_create(session: SessionDep, product: ProductBase):
    return await create_product(session, product)
