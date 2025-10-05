from fastapi import FastAPI, Cookie
from typing import Annotated
app = FastAPI()

## Cookie Parameters
@app.get("/products/recommendations")
async def get_recommendations(session_id: Annotated[str | None, Cookie()] = None):
  if session_id:
    return {"message": f"Recommendations for session {session_id}", "session_id": session_id}
  return {"message": "No session ID provided, showing default recommendations"}

# curl -H "Cookie: session_id=abc123" http://127.0.0.1:8000/products/recommendations