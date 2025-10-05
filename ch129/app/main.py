from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from app.resume.routers import router as resume_router
from fastapi.templating import Jinja2Templates
from app.db.config import SessionDep
from app.resume.services import get_all_resumes
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

app.include_router(resume_router)

INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
    "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya",
    "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim",
    "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand",
    "West Bengal", "Delhi", "Jammu and Kashmir", "Ladakh"
]

PREFERRED_LOCATIONS = [
    "Bangalore", "Hyderabad", "Mumbai", "Delhi", "Chennai",
    "Pune", "Kolkata", "Ahmedabad", "Jaipur"
]

@app.get("/create", response_class=HTMLResponse)
def form(request: Request):
    return templates.TemplateResponse("upload_resume.html", {
        "request": request,
        "indian_states": INDIAN_STATES,
        "preferred_location_options": PREFERRED_LOCATIONS
    })

@app.get("/", response_class=HTMLResponse)
async def resume_list(request: Request, session: SessionDep):
    resumes = await get_all_resumes(session)
    return templates.TemplateResponse("resume_list.html", {
        "request": request,
        "resumes": resumes
    })