from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

# ## Nested Body Models
## Submodel
class Category(BaseModel):
  name : str = Field(
    title="Category Name",
    description="The name of the product category",
    max_length=50,
    min_length=1
  )
  description: str | None = Field(
        default=None,
        title="Category Description",
        description="A brief description of the category",
        max_length=200
    )
  
## Model which will use Submodel
class Product(BaseModel):
    name: str = Field(
        title="Product Name",
        description="The name of the product",
        max_length=100,
        min_length=1
    )
    price: float = Field(
        gt=0,
        title="Product Price",
        description="The price in USD, must be greater than zero"
    )
    stock: int | None = Field(
        default=None,
        ge=0,
        title="Stock Quantity",
        description="Number of items in stock, must be non-negative"
    )
    category : Category | None = Field(
       default=None,
       title="Product Category",
       description="The category to which the product belongs"
    )

@app.post("/products")
async def create_product(product: Product):
    return product

# # ## Attributes with lists of submodels
# class Category(BaseModel):
#     name: str = Field(
#         title="Category Name",
#         description="The name of the product category",
#         max_length=50,
#         min_length=1
#     )
#     description: str | None = Field(
#         default=None,
#         title="Category Description",
#         description="A brief description of the category",
#         max_length=200
#     )

# class Product(BaseModel):
#     name: str = Field(
#         title="Product Name",
#         description="The name of the product",
#         max_length=100,
#         min_length=1
#     )
#     price: float = Field(
#         gt=0,
#         title="Product Price",
#         description="The price in USD, must be greater than zero"
#     )
#     stock: int | None = Field(
#         default=None,
#         ge=0,
#         title="Stock Quantity",
#         description="Number of items in stock, must be non-negative"
#     )
#     category: list[Category] | None = Field(
#        default=None,
#        title="Product Category",
#        description="The category to which the product belongs"
#     )

# @app.post("/products")
# async def create_product(product: Product):
#     return product