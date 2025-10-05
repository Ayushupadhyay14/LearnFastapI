from fastapi import FastAPI
from app.resume.routers import router as resume_router

app = FastAPI()

app.include_router(resume_router)