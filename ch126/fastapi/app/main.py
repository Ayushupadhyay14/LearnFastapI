from fastapi import FastAPI
from app.resume.routers import router as resume_router
from fastapi.middleware.cors import CORSMiddleware
from decouple import config

DEBUG = config("DEBUG", cast=bool)

app = FastAPI(
  title="Resume Uploader API",
  docs_url="/docs" if DEBUG else None,
  redoc_url="/redoc" if DEBUG else None,
  openapi_url="/openapi.json" if DEBUG else None
)
FRONTEND_URL = config("FRONTEND_URL")
# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume_router)