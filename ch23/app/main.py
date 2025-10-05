from typing import Annotated
from fastapi import FastAPI, Header, Body
from pydantic import BaseModel, Field
app = FastAPI()

## Headers with a Pydantic Model

class ProductHeaders(BaseModel):
  authorization: str
  accept_language: str | None = None
  x_tracking_id: list[str] = []

@app.get("/products")
async def get_product(headers: Annotated[ProductHeaders, Header()]):
    return {
        "headers": headers
    }

# curl -H "Authorization: Bearer token123" -H "Accept-Language: en-US" -H "X-Tracking-Id: track1" -H "X-Tracking-Id: track2" http://127.0.0.1:8000/products

# Forbidding Extra Headers
# class ProductHeaders(BaseModel):
#   model_config = {"extra":"forbid"}
#   authorization: str
#   accept_language: str | None = None
#   x_tracking_id: list[str] = []

# @app.get("/products")
# async def get_product(headers: Annotated[ProductHeaders, Header()]):
#     return {
#         "headers": headers
#     }

# curl -H "Authorization: Bearer token123" -H "Accept-Language: en-US" -H "X-Tracking-Id: track1" -H "X-Tracking-Id: track2" -H "extra-header: h123" http://127.0.0.1:8000/products