from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated

app = FastAPI()

# Dependencies with yield

class OwnerError(Exception):
  pass

def get_username():
  try:
    yield "Raj"
  except OwnerError as e:
    raise HTTPException(status_code=400, detail=f"Owner error: {e}")
  
@app.get("/items/{item_id}")  
def get_items(item_id: str, username: Annotated[str, Depends(get_username)]):
    data = {
    "pressure-cooker": 
      {"description": "Essential for making dal-chawal", 
       "owner": "Priya" },
    "scooty": 
      {"description": "Zippy ride for city streets", 
       "owner": "Raj" },
    }

    if item_id not in data:
      raise HTTPException(status_code=404, detail="Item not found")
    
    item = data[item_id]

    if item["owner"] != username :
      raise OwnerError(username)
    
    return item
  
