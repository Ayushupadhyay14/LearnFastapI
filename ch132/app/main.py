from fastapi import FastAPI
from app.core.log_config import logger
from fastapi.exceptions import RequestValidationError
from app.core.errors import global_exception_handler, validation_exception_handler

app = FastAPI()

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

@app.get("/")
async def root():
  return {"msg": "Welcome to FastAPI"}

@app.get("/items/{item_id}")
def get_item(item_id: int):  
    return {"item_id": item_id}

@app.get("/product/{price}")
def get_item(price: float):
    return {"price": price}

@app.get("/crash")
def crash():
    x = 1 / 0  # ZeroDivisionError