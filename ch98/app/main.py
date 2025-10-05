from fastapi import FastAPI, Request, Form
from contextlib import asynccontextmanager
from app.db.config import create_tables, SessionDep
from app.product.services import create_product, get_all_products
from app.product.models import ProductCreate, ProductOut

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()  
    yield 

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
template = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request, session: SessionDep):
    products = get_all_products(session)
    return template.TemplateResponse("product_list.html", {"request": request, "products": products})

@app.post("/create", response_class=HTMLResponse)
def create(request: Request, session: SessionDep, title: str = Form(...), description: str = Form(...)):
    new_product = ProductCreate(title=title, description=description)
    create_product(session, new_product)
    return RedirectResponse("/", status_code=302)
    
## You can keep below if you need API as well
# @app.post("/products", response_model=ProductOut)
# def product_create(session: SessionDep, new_product: ProductCreate):
#    product = create_product(session, new_product)
#    return product

# @app.get("/products", response_model=list[ProductOut])
# def all_products(session: SessionDep):
#   products = get_all_products(session)
#   return products