from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

# ## Using Field-level Examples
# class Product(BaseModel):
#     name: str = Field(examples=["Moto E"])
#     price: float = Field(examples=[23.56])
#     stock: int | None = Field(default=None, examples=[43])

# @app.post("/products")
# async def create_product(product: Product):
#     return product

## Using Pydantic’s json_schema_extra
class Product(BaseModel):
  name: str
  price: float
  stock: int | None = None

  model_config = {
    "json_schema_extra": {
      "examples": [
        {
          "name": "Moto E",
          "price": 34.56,
          "stock": 45
        }
      ]
    }
  }

@app.post("/products")
async def create_product(product: Product):
    return product