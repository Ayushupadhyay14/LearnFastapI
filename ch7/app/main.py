from fastapi import FastAPI

app = FastAPI()

## Order matters

@app.get("/product/rode_nt_usb")
async def single_product():
    return {"response":"Single Data Fetched"}

@app.get("/product/{product_title}")
async def single_product(product_title:str):
    return {"response":"Single Data Fetched", "product_title": product_title}
