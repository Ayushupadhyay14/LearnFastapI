from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
  return {"msg": "Project Online"}

@app.get("/contact")
async def contact():
  return {"msg": "Contact Online"}