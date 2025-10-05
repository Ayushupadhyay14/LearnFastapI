from fastapi import FastAPI, Depends
from typing import Annotated

app = FastAPI()

# Creating Dependency Function
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
  return {"q": q, "skip": skip, "limit": limit}

# Using Dependency in endpoints
@app.get("/items")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
  return commons

@app.get("/users")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
  return commons

# Create a type alias
CommonsDep = Annotated[dict, Depends(common_parameters)]

@app.get("/products")
async def read_products(commons: CommonsDep):
  return commons

@app.get("/carts")
async def read_carts(commons: CommonsDep):
  return commons