from fastapi import FastAPI
from enum import Enum
app = FastAPI()

## Predefined values
# Define an Enum class with allowed product categories
class ProductCategory(str, Enum):
    books = "books"
    clothing = "clothing"
    electronics = "electronics"

# Use the Enum as the type for the path parameter
@app.get("/product/{category}")
async def get_products(category:ProductCategory):
    return {"response": "Products fetched", "category": category}

## Working with Python enumerations
# class ProductCategory(str, Enum):
#     books = "books"
#     clothing = "clothing"
#     electronics = "electronics"

# @app.get("/product/{category}")
# async def get_products(category:ProductCategory):
#     if category == ProductCategory.books:
#         return {"category": category, "message": "Books are awesome!"}
#     elif category.value == "clothing":
#         return {"category": category, "message": "Fashion trends here!"}
#     elif category == ProductCategory.electronics.value:
#         return {"category": category, "message": "Latest gadgets available!"}
#     else:
#         return {"category": category, "message": "Unknown category"}