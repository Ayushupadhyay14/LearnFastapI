from fastapi import FastAPI, Cookie, Body
from typing import Annotated
from pydantic import BaseModel, Field
app = FastAPI()

# ## Cookies with a Pydantic Model
# class ProductCookies(BaseModel):
#   session_id: str
#   preferred_category: str | None = None
#   tracking_id: str | None = None

# @app.get("/products/recommendations")
# async def get_recommendations(cookies: Annotated[ProductCookies, Cookie()]):
#   response = {"session_id": cookies.session_id}
#   if cookies.preferred_category:
#     response["message"] = f"Recommendations for {cookies.preferred_category} products"
#   else:
#     response["message"] = f"Default recommendations for session {cookies.session_id}"
#   if cookies.tracking_id:
#       response["tracking_id"] = cookies.tracking_id
#   return response

# curl -H "Cookie: session_id=abc123; preferred_category=Electronics; tracking_id=xyz789" http://127.0.0.1:8000/products/recommendations

## Forbidding Extra Cookies
# class ProductCookies(BaseModel):
#   model_config = {"extra": "forbid"}
#   session_id: str
#   preferred_category: str | None = None
#   tracking_id: str | None = None

# @app.get("/products/recommendations")
# async def get_recommendations(cookies: Annotated[ProductCookies, Cookie()]):
#   response = {"session_id": cookies.session_id}
#   if cookies.preferred_category:
#     response["message"] = f"Recommendations for {cookies.preferred_category} products"
#   else:
#     response["message"] = f"Default recommendations for session {cookies.session_id}"
#   if cookies.tracking_id:
#       response["tracking_id"] = cookies.tracking_id
#   return response

# Combining Cookie with Body Parameters
class ProductCookies(BaseModel):
  model_config = {"extra": "forbid"}
  session_id: str = Field(title="Session ID", description="User session identifier")
  preferred_category: str | None = Field(default=None, title="Preferred Category", description="User's preferred product category")

class PriceFilter(BaseModel):
    min_price: float = Field(ge=0, title="Minimum Price", description="Minimum price for recommendations")
    max_price: float | None = Field(default=None, title="Maximum Price", description="Maximum price for recommendations")

@app.post("/products/recommendations")
async def get_recommendations(
   cookies: Annotated[ProductCookies, Cookie()],
   price_filter: Annotated[PriceFilter, Body(embed=True)]
   ):
  response = {"session_id": cookies.session_id}
  if cookies.preferred_category:
    response["category"] = cookies.preferred_category
  response["price_range"] = {
        "min_price": price_filter.min_price,
        "max_price": price_filter.max_price
    }
  response["message"] = f"Recommendations for session {cookies.session_id} with price range {price_filter.min_price} to {price_filter.max_price or 'unlimited'}"
  return response

# curl -X POST -H "Cookie: session_id=abc123; preferred_category=Electronics" -H "Content-Type: application/json" -d "{\"price_filter\":{\"min_price\":50.0,\"max_price\":1000.0}}" http://127.0.0.1:8000/products/recommendations