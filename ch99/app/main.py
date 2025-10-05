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
def home(request: Request):
    return template.TemplateResponse("index.html", {"request": request})

@app.get("/form", response_class=HTMLResponse)
def load_form(request: Request):
    return template.TemplateResponse("product_form.html", {"request": request})

@app.get("/products/list", response_class=HTMLResponse)
def product_list(request: Request, session: SessionDep):
    products = get_all_products(session)
    return template.TemplateResponse("product_list.html", {"request": request, "products": products})

@app.post("/products", response_class=HTMLResponse)
def product_create(request: Request, session: SessionDep, title: str = Form(...), description: str = Form(...)):
    product_data = ProductCreate(title=title, description=description)
    create_product(session, product_data)
    products = get_all_products(session)
    return template.TemplateResponse("product_list.html", {"request": request, "products": products})