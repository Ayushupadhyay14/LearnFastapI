from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.config import init_db
from app.account.routers import router as account_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(account_router)