from fastapi import FastAPI

app = FastAPI()

## Parameter with Type
@app.get("/product/{product_id}")
async def single_product(product_id):
    return {"response":"Single Data Fetched", "product_id": product_id}

# @app.get("/product/{product_id}")
# async def single_product(product_id:int):
#     return {"response":"Single Data Fetched", "product_id": product_id}

# @app.get("/product/{product_title}")
# async def single_product(product_title:str):
#     return {"response":"Single Data Fetched", "product_title": product_title}