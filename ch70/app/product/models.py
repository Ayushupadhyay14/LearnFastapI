from sqlmodel import Field, SQLModel

class Product(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str