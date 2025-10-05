from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
  return {"msg": "Project Online 1"}

@app.get("/contact")
async def contact():
  return {"msg": "Contact Online 1"}
