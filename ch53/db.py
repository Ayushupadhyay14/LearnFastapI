from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = "sqlite+aiosqlite:///./sqlite.db"

engine = create_async_engine(DATABASE_URL, echo=True)

