from fastapi import FastAPI, Depends, Header, HTTPException
from typing import Annotated

app = FastAPI()

# Dependencies in Path Operation Decorators
async def verify_token(x_token: Annotated[str, Header()]):
  if x_token != "my-secret-token":
    raise HTTPException (status_code=400, detail="X-Token header invalid")
  
@app.get("/items", dependencies=[Depends(verify_token)])
async def read_items():
  return {"data": "All Items"}