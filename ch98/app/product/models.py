from sqlmodel import Field, SQLModel

class ProductBase(SQLModel):
    title: str
    description: str

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int
    
class Product(ProductBase, table=True):
    id: int = Field(primary_key=True)