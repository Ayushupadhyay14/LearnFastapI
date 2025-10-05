from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from decouple import config
from app.account.models import User

DB_USER = config("DB_USER")
DB_PASS = config("DB_PASS")
DB_NAME = config("DB_NAME")
DB_PORT = config("DB_PORT", cast=int)

MONGO_URI = f"mongodb://{DB_USER}:{DB_PASS}@localhost:{DB_PORT}/{DB_NAME}?authSource=admin"

async def init_db():
    client = AsyncIOMotorClient(MONGO_URI)
    await init_beanie(database=client[DB_NAME], document_models=[User])