from fastapi import APIRouter
from typing import List
from app.db.config import SessionDep
from app.product.schemas import ProductBase, ProductRead, ProductUpdate
from app.product.services import (
    create_product, get_all_products,
    get_product, update_product, delete_product
)

router = APIRouter(prefix="/products", tags=["Product"])

@router.post("/create", response_model=ProductRead)
async def product_create(session: SessionDep, product: ProductBase):
    return await create_product(session, product)

@router.get("/", response_model=List[ProductRead])
async def product_list(session: SessionDep):
    return await get_all_products(session)

@router.get("/{product_id}", response_model=ProductRead)
async def product_detail(product_id: int, session: SessionDep):
    return await get_product(product_id, session)

@router.put("/{product_id}", response_model=ProductRead)
async def product_update(product_id: int, data: ProductUpdate, session: SessionDep):
    return await update_product(product_id, data, session)

@router.delete("/{product_id}")
async def product_delete(product_id: int, session: SessionDep):
    return await delete_product(product_id, session)
