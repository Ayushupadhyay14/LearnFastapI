from fastapi import FastAPI

app = FastAPI()

# GET Request
## Read or Fetch All Data
@app.get("/product")
async def all_products():
  return {"response": "All Products"}

## Read or Fetch Single Data
@app.get("/product/{product_id}")
async def single_product(product_id:int):
  return {"response":"Single Data Fetched", "product_id": product_id}

# POST Request
## Create or Insert Data
@app.post("/product")
async def create_product(new_product: dict):
  return {"response": "Product Created", "new product": new_product}

# PUT Request
## Update Complete Data
@app.put("/product/{product_id}")
async def update_product(new_updated_product: dict, product_id: int):
  return {"response":"Complete Data Updated", "product_id": product_id, "new updated product":new_updated_product}

# PATCH Request
## Update Partial Data
@app.patch("/product/{product_id}")
async def partial_product(new_updated_product: dict, product_id: int):
  return {"response":"Partial Data Updated", "product_id": product_id, "new updated product":new_updated_product}

# DELETE Request
## Delete Data
@app.delete("/product/{product_id}")
def delete_product(product_id: int):
    return {"response":"Data Deleted", "product_id": product_id}