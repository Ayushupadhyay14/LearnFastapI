from fastapi import FastAPI
from app.middlewares import my_first_middleware, my_second_middleware

app = FastAPI()

app.middleware("http")(my_second_middleware)
app.middleware("http")(my_first_middleware)


@app.get("/users")
async def get_users():
  print("Endpoint: Inside get_users endpoint")
  return {"data": "All Users Data"}

@app.get("/products")
async def get_products():
    print("Endpoint: Inside get_products endpoint")
    return {"data": "All products data"}



