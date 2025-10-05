from typing import List
from fastapi import APIRouter, UploadFile, Form, File
from app.db.config import SessionDep
from app.resume.schemas import ResumeCreate, ResumeOut, GenderEnum
from app.resume.services import create_resume, get_all_resumes

router = APIRouter(prefix="/resumes", tags=["Resume"])

@router.post("/upload", response_model=ResumeOut)
async def upload_resume(
    *,
    name: str = Form(...),
    email: str = Form(...),
    dob: str = Form(...),
    state: str = Form(...),
    gender: GenderEnum = Form(...),
    preferred_locations: List[str] = Form(...),
    image: UploadFile = File(...),
    resume_file: UploadFile = File(...),
    session: SessionDep
):
  data = ResumeCreate(
        name=name,
        email=email,
        dob=dob,
        state=state,
        gender=gender,
        preferred_locations=preferred_locations,
    )
  return await create_resume(session, data, image, resume_file)

@router.get("/", response_model=List[ResumeOut])
async def list_resumes(session: SessionDep):
    resumes = await get_all_resumes(session)
    return resumes
