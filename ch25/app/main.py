from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Any

app = FastAPI()

class Product(BaseModel):
  id: int
  name: str
  price : float
  stock: int | None = None

class ProductOut(BaseModel):
  name: str
  price : float

## without response_model Parameter
# @app.get("/products/")
# async def get_products():
#   return {"id": 1, "name": "Moto E", "price": 33.44, "stock": 5}

# with response_model Parameter
@app.get("/products/", response_model=Product)
async def get_products():
  return {"id": 1, "name": "Moto E", "price": 33.44, "stock": 5}


# @app.get("/products/", response_model=List[Product])
# async def get_products():
#   return [
#        {"id": 1, "name": "Moto E", "price": 33.44, "stock": 5},
#        {"id": 2, "name": "Redmi 4", "price": 55.33, "stock": 7}
#     ]

# @app.get("/products/", response_model=List[Product])
# async def get_products():
#   return [
#        {"id": 1, "name": "Moto E", "price": 33.44, "stock": 5, "description": "Hello Desc1"},
#        {"id": 2, "name": "Redmi 4", "price": 55.33, "stock": 7, "description": "Hello Desc2"}
#     ]

# @app.post("/products/", response_model=Product)
# async def create_product(product: Product):
#   return product

# class BaseUser(BaseModel):
#     username: str
#     full_name: str | None = None

# class UserIn(BaseUser):
#     password: str

# @app.post("/users/", response_model=BaseUser)
# async def create_user(user: UserIn):
#   return user

# @app.post("/products/", response_model=Product)
# async def create_product(product: Product) -> Any:
#   return product

# @app.post("/products/", response_model=None)
# async def create_product(product: Product) -> Any:
#   return product