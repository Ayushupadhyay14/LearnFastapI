from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI()

app.add_middleware(HTTPSRedirectMiddleware)
# app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1"])

@app.get("/users")
async def get_users():
  print("Endpoint: Inside get_users endpoint")
  return {"data": "All Users Data"}

@app.get("/products")
async def get_products():
    print("Endpoint: Inside get_products endpoint")
    return {"data": "All products data"}


# curl -i http://127.0.0.1:8000/users
# curl -H "Host: localhost" http://127.0.0.1:8000/users
