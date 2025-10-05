from fastapi import FastAPI, Depends
from app.routers import router, verify_token

app = FastAPI()

# Dependencies for a Group of Path Operations
# app.include_router(router)

app.include_router(router, dependencies=[Depends(verify_token)])

