import pytest
import pytest_asyncio
import os
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import text
from app.main import app
from app.db.config import Base, get_session
from typing import AsyncGenerator

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(BASE_DIR, "test_sqlite.db")
DATABASE_URL = f"sqlite+aiosqlite:///{db_path}"

engine = create_async_engine(DATABASE_URL, echo=True)

async_test_session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

# Override FastAPI's get_session dependency to use the test database
async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_test_session() as test_session:
        yield test_session

app.dependency_overrides[get_session] = override_get_session

# Initialize FastAPI TestClient for testing API endpoints
client = TestClient(app)

# Pytest fixtures
@pytest_asyncio.fixture(scope="function")
async def setup_database():
    async with engine.begin() as conn:
         await conn.run_sync(Base.metadata.drop_all)  # Drop all tables
         await conn.run_sync(Base.metadata.create_all)  # Create all tables
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # Drop all tables after test
    await engine.dispose()  # Close all database connections
    if os.path.exists(db_path):
      for _ in range(5):  # Retry up to 5 times for Windows file locking
        try:
            os.remove(db_path)
            break
        except PermissionError:
            import time
            time.sleep(0.5)

@pytest_asyncio.fixture
async def test_session(setup_database) -> AsyncGenerator[AsyncSession, None]:
  async with async_test_session() as session:
    # Clear products table to ensure no residual data
    await session.execute(text("DELETE FROM products"))
    await session.commit()
    yield session

@pytest_asyncio.fixture
def test_client():
   return client
        
        






