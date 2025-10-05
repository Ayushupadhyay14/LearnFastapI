from fastapi import FastAPI, Depends
from typing import Annotated

app = FastAPI()

# sync dependency
def sync_dep():
  return {"message": "I am sync"}

# async dependency
async def async_dep():
  return {"message": "I am async"}

@app.get("/test/")
async def test(
  sync_result: Annotated[dict, Depends(sync_dep)],
  async_result: Annotated[dict, Depends(async_dep)],
):
  return {"sync": sync_result, "async": async_result}