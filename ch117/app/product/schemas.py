from pydantic import BaseModel
from datetime import datetime

class ProductBase(BaseModel):
    title: str

class ProductRead(ProductBase):
    id: int
    created_at: datetime
    model_config = {
        "from_attributes": True
        }