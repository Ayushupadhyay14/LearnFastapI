from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

## Without Pydantic
## Create or Insert Data
@app.post("/product")
async def create_product(new_product: dict):
  return new_product


## With Pydantic
# # Define the Product model
class Product(BaseModel):
  id: int
  name: str
  price: float
  stock: int | None = None

# @app.post("/product")
# async def create_product(new_product: Product):
#   return new_product

# ## Access Attribute inside Function
# @app.post("/product")
# async def create_product(new_product: Product):
#   print(new_product.id)
#   print(new_product.name)
#   print(new_product.price)
#   print(new_product.stock)
#   return new_product

## Add new calculated attribute
# @app.post("/product")
# async def create_product(new_product: Product):
#   product_dict = new_product.model_dump()
#   price_with_tax = new_product.price + (new_product.price * 18 / 100)
#   product_dict.update({"price_with_tax": price_with_tax})
#   return product_dict

## Combining Request Body with Path Parameters
# @app.put("/products/{product_id}")
# async def update_product(product_id: int, new_updated_product: Product):
#     return {"product_id": product_id, "new_updated_product":new_updated_product}

## Adding Query Parameters
# @app.put("/products/{product_id}")
# async def update_product(product_id: int, new_updated_product: Product, discount: float | None = None):
#     return {"product_id": product_id, "new_updated_product": new_updated_product, "discount": discount}