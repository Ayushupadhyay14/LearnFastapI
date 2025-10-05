from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Product(BaseModel):
  id: int
  name: str
  price : float
  stock: int | None = None

class ProductOut(BaseModel):
  name: str
  price : float


# # Without Return Type
# @app.get("/products/")
# async def get_products():
#     return [
#        {"status": "OK"},
#        {"status": 200}
#     ]

## Return type annotation
@app.get("/products/")
async def get_products() -> Product:
    return {"id": 1, "name": "Moto E", "price": 33.44, "stock": 5}

# @app.get("/products/")
# async def get_products() -> Product:
#     return {"id": 1, "name": "Moto E", "price": 33.44}

# @app.get("/products/")
# async def get_products() -> Product:
#     return {"id": 1, "name": "Moto E", "price": 33.44, "stock": 5, "description": "This is moto e"}

# @app.get("/products/")
# async def get_products() -> List[Product]:
#     return [
#        {"id": 1, "name": "Moto E", "price": 33.44, "stock": 5},
#        {"id": 2, "name": "Redmi 4", "price": 55.33, "stock": 7}
#     ]

# @app.get("/products/")
# async def get_products() -> List[Product]:
#     return [
#        {"id": 1, "name": "Moto E", "price": 33.44, "stock": 5, "description": "Hello Desc1"},
#        {"id": 2, "name": "Redmi 4", "price": 55.33, "stock": 7, "description": "Hello Desc2"}
#     ]

# @app.post("/products/")
# async def create_product(product: Product) -> Product:
#   return product

# @app.post("/products/")
# async def create_product(product: Product) -> ProductOut:
#   return product

# class BaseUser(BaseModel):
#     username: str
#     full_name: str | None = None

# class UserIn(BaseUser):
#     password: str

# @app.post("/users/")
# async def create_user(user: UserIn) -> BaseUser:
#   return user