from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {
  "apple": "A juicy fruit", 
  "banana": "A yellow delight"
  }

## Using HTTPException
@app.get("/items/{item_id}")
async def read_item(item_id: str):
  if item_id not in items:
    raise HTTPException(status_code=404, detail="Item not found")
  return items[item_id]

# # Adding Custom Header
# @app.get("/items/{item_id}")
# async def read_item(item_id: str):
#   if item_id not in items:
#     raise HTTPException(
#       status_code=404, 
#       detail="Item not found",
#       headers={"x-error-type": "itemmissing"}
#       )
#   return items[item_id]

