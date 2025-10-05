from fastapi import FastAPI
from app.middlewares import CustomLoggingMiddleware

app = FastAPI()

app.add_middleware(CustomLoggingMiddleware, prefix="CUSTOM_LOG")

@app.get("/users")
async def get_users():
  print("Endpoint: Inside get_users endpoint")
  return {"data": "All Users Data"}

@app.get("/products")
async def get_products():
    print("Endpoint: Inside get_products endpoint")
    return {"data": "All products data"}



