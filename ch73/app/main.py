from fastapi import FastAPI, Request

app = FastAPI()

# First Middleware
@app.middleware("http")
async def my_first_middleware(request: Request, call_next):
  print("1st Middleware: Before processing the request")
  response = await call_next(request)
  print("1st Middleware: After processing the request, before returning response")
  return response

# Second Middleware
@app.middleware("http")
async def my_second_middleware(request: Request, call_next):
  print("2nd Middleware: Before processing the request")
  response = await call_next(request)
  print("2nd Middleware: After processing the request, before returning response")
  return response

@app.get("/users")
async def get_users():
  print("Endpoint: Inside get_users endpoint")
  return {"data": "All Users Data"}

@app.get("/products")
async def get_products():
    print("Endpoint: Inside get_products endpoint")
    return {"data": "All products data"}



