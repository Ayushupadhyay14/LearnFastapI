from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

from app.user import models as user_models
from app.product import models as product_models