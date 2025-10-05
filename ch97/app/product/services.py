from sqlmodel import Session, select
from app.product.models import Product, ProductOut

def create_product(session: Session, new_product: Product) -> ProductOut:
  product = Product(title=new_product.title, description=new_product.description)
  session.add(product)
  session.commit()
  session.refresh(product)
  return product
  
def get_all_products(session: Session) -> list[ProductOut]:
    stmt = select(Product)
    product = session.exec(stmt)
    return product.all()