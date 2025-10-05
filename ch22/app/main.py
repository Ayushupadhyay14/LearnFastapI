from fastapi import FastAPI, Header
from typing import Annotated
app = FastAPI()

## Header Parameters
@app.get("/products")
async def get_products(user_agent: Annotated[str|None, Header()] = None):
  return user_agent

# curl -H "User-Agent: Mozilla/5.0" http://127.0.0.1:8000/products

## Handling Duplicate Headers
# @app.get("/products")
# async def get_product(x_product_token: Annotated[list[str] | None, Header()] = None):
#     return {
#         "x_product_token": x_product_token or []
#     }

# curl -H "X-Product-Token: token1" -H "X-Product-Token: token2" http://127.0.0.1:8000/products