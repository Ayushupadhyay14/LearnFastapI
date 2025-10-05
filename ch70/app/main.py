from fastapi import FastAPI
from app.user.models import User
from app.product.models import Product
from app.db.config import create_tables
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
  create_tables()
  yield

app = FastAPI(lifespan=lifespan)