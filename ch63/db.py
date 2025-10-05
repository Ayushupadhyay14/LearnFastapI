from sqlmodel import create_engine

DATABASE_URL = "sqlite:///sqlite.db"

engine = create_engine(DATABASE_URL, echo=True)