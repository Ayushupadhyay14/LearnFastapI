from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.config import create_tables
from app.product.routers import router as product_router
from app.product.models import Product

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(product_router)

@app.get("/")
async def root():
  return {"msg": "Changed to Fine"}