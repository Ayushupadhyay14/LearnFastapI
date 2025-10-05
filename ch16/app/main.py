from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Annotated
app = FastAPI()

## Multiple Body Parameters
class Product(BaseModel):
  name: str
  price:float
  stock: int | None = None

class Seller(BaseModel):
  username: str
  full_name: str | None = None

# @app.post("/product")
# async def create_product(product: Product, seller:Seller):
#   return {"product": product, "seller":seller}

## Make Body Optional
# @app.post("/product")
# async def create_product(product: Product, seller:Seller | None = None):
#   return {"product": product, "seller":seller}

## Singular values in body
# @app.post("/product")
# async def create_product(
#   product: Product, 
#   seller:Seller, 
#   sec_key: Annotated[str, Body()]
#   ):
#   return {"product": product, "seller":seller, "sec_key":sec_key}

## Embed a single body parameter
## Without Embed
# @app.post("/product")
# async def create_product(product: Product):
#   return product

## With Embed
# @app.post("/product")
# async def create_product(product: Annotated[Product, Body(embed=True)]):
#   return product