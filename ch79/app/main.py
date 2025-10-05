from fastapi import FastAPI
from app.user.routers import router as user_routers
from app.product.routers import router as product_routers

app = FastAPI()

# app.include_router(user_routers, tags=["users"])
# app.include_router(product_routers, tags=["products"])

app.include_router(user_routers)
app.include_router(product_routers)

@app.get("/")
async def root():
  return {"data": "Root"}
