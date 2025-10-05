from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.config import create_tables
from app.account.routers import router as account_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(account_router)