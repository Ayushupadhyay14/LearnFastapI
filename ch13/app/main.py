from fastapi import FastAPI, Query
from typing import Annotated
from pydantic import AfterValidator

app = FastAPI()

PRODUCTS = [
    {"id": 1, "title": "Ravan Backpack", "price": 109.95, "description": "Perfect for everyday use and forest walks."},
    {"id": 2, "title": "Slim Fit T-Shirts", "price": 22.3, "description": "Comfortable, slim-fitting casual shirts."},
    {"id": 3, "title": "Cotton Jacket", "price": 55.99, "description": "Great for outdoor activities and gifting."},
]

# Basic Query Parameter
# @app.get("/products")
# async def get_products(search:str | None = None):
#   if search:
#     search_lower = search.lower()
#     filtered_products = []
#     for product in PRODUCTS:
#       if search_lower in product["title"].lower(): 
#         filtered_products.append(product)
#     return filtered_products
#   return PRODUCTS

# Validation without Annotated
# @app.get("/products")
# async def get_products(search:str | None = Query(default=None, max_length=5)):
#   if search:
#     search_lower = search.lower()
#     filtered_products = []
#     for product in PRODUCTS:
#       if search_lower in product["title"].lower(): 
#         filtered_products.append(product)
#     return filtered_products
#   return PRODUCTS

# Validation with Annotated
# @app.get("/products")
# async def get_products(
#   search: 
#     Annotated[
#       str | None, 
#       Query(max_length=5)
#       ] = None):
#   if search:
#     search_lower = search.lower()
#     filtered_products = []
#     for product in PRODUCTS:
#       if search_lower in product["title"].lower(): 
#         filtered_products.append(product)
#     return filtered_products
#   return PRODUCTS

# Why use Annotated
## Clear separation of the type
## Better support in some editors and tools for showing metadata and validations directly in the type hints
## Requires Python 3.9+ and FastAPI 0.95+; more modern and recommended approach
## FastAPI 0.95+ officially recommends using Annotated for dependencies and parameters

# # Required Parameter
# @app.get("/products/")
# async def get_products(search: Annotated[str, Query(min_length=3)]):
#     if search:
#         search_lower = search.lower()
#         filtered_products = []
#         for product in PRODUCTS:
#             if search_lower in product["title"].lower():
#                 filtered_products.append(product)
#         return filtered_products
#     return PRODUCTS

## Add regular expressions
# @app.get("/products/")
# async def get_products(search: Annotated[str | None, Query(min_length=3, pattern="^[a-z]+$")] = None):
#     if search:
#         search_lower = search.lower()
#         filtered_products = []
#         for product in PRODUCTS:
#             if search_lower in product["title"].lower():
#                 filtered_products.append(product)
#         return filtered_products
#     return PRODUCTS

# # Multiple Search Terms (List)
# @app.get("/products")
# async def get_products(search: Annotated[list[str] | None, Query()] = None):
#   if search:
#     filtered_products = []
#     for product in PRODUCTS:
#       for s in search:
#         if s.lower() in product["title"].lower():
#           filtered_products.append(product)
#     return filtered_products
#   return PRODUCTS

## Alias parameters
# @app.get("/products/")
# async def get_products(search: Annotated[str | None, Query(alias="q")] = None):
#     if search:
#         search_lower = search.lower()
#         filtered_products = []
#         for product in PRODUCTS:
#             if search_lower in product["title"].lower():
#                 filtered_products.append(product)
#         return filtered_products
#     return PRODUCTS

# # Adding Metadata
# @app.get("/products/")
# async def get_products(search: Annotated[
#         str | None,
#         Query(alias="q", title="Search Products", description="Search by product title")
#     ] = None
#     ):
#     if search:
#         search_lower = search.lower()
#         filtered_products = []
#         for product in PRODUCTS:
#             if search_lower in product["title"].lower():
#                 filtered_products.append(product)
#         return filtered_products
#     return PRODUCTS

# # Deprecating parameters
# @app.get("/products/")
# async def get_products(search: Annotated[
#         str | None,
#         Query(deprecated=True)
#     ] = None
#     ):
#     if search:
#         search_lower = search.lower()
#         filtered_products = []
#         for product in PRODUCTS:
#             if search_lower in product["title"].lower():
#                 filtered_products.append(product)
#         return filtered_products
#     return PRODUCTS

## Custom Validation
# def check_valid_id(id: str):
#   if not id.startswith("prod-"):
#     raise ValueError("ID must start with 'prod-'")
#   return id

# @app.get("/products/")
# async def get_products(id: Annotated[str | None, AfterValidator(check_valid_id)] = None):
#     if id:
#         return {"id": id, "message": "Valid product ID"}
#     return {"message": "No ID provided"}