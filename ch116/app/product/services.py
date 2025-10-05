from app.product.models import Product
from app.product.schemas import ProductBase, ProductUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

async def create_product(session: AsyncSession, product: ProductBase):
    new_product = Product(title=product.title)
    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)
    return new_product

async def get_all_products(session: AsyncSession):
    result = await session.execute(select(Product))
    return result.scalars().all()

async def get_product(product_id: int, session: AsyncSession):
    product = await session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

async def update_product(product_id: int, data: ProductUpdate, session: AsyncSession):
    product = await session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if data.title is not None:
        product.title = data.title

    await session.commit()
    await session.refresh(product)
    return product

async def delete_product(product_id: int, session: AsyncSession):
    product = await session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    await session.delete(product)
    await session.commit()
    return {"detail": "Product deleted successfully"}
