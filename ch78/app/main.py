from fastapi import FastAPI
from app.user.routers import router as user_routers
from app.product.routers import router as product_routers

app = FastAPI()

app.include_router(user_routers)
app.include_router(product_routers)

@app.get("/")
async def root():
  return {"data": "Root"}


# @app.get("/users")
# async def get_all_users():
#   return {"data": "All Users"}

# @app.get("/users/me")
# async def get_current_user():
#   return {"data": "Current User"}

# @app.get("/users/{user_id}")
# async def get_single_user(user_id: int):
#   return {"data": "Single User"}

# @app.get("/products")
# async def get_all_products():
#   return {"data": "All Products"}

# @app.get("/products/{product_id}")
# async def get_single_product(product_id: int):
#   return {"data": "Single Product"}