from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.config import create_tables, SessionDep
from app.product.services import create_product, get_all_products
from app.product.models import ProductCreate, ProductOut

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()  
    yield 

app = FastAPI(lifespan=lifespan)

@app.post("/products", response_model=ProductOut)
def product_create(session: SessionDep, new_product: ProductCreate):
   product = create_product(session, new_product)
   return product

@app.get("/products", response_model=list[ProductOut])
def all_products(session: SessionDep):
  products = get_all_products(session)
  return products