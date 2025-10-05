from fastapi import FastAPI, Depends, Header, HTTPException
from typing import Annotated

# Global Dependencies
async def verify_token(x_token: Annotated[str, Header()]):
  if x_token != "my-secret-token":
    raise HTTPException (status_code=400, detail="X-Token header invalid")

app = FastAPI(dependencies=[Depends(verify_token)])

@app.get("/items")
async def read_items():
    return {"data": "All Items"}

@app.get("/products")
async def read_products():
    return {"data": "All Products"}