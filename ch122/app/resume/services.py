from fastapi import HTTPException, UploadFile
from app.resume.models import Resume
from app.resume.schemas import ResumeCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.resume.utils import get_file_url, save_upload_file

async def create_resume(session: AsyncSession, data: ResumeCreate, image: UploadFile, resume_file: UploadFile,):
  stmt = select(Resume).where(Resume.email == data.email)
  result = await session.scalars(stmt)
  if result.first():
      raise HTTPException(status_code=400, detail="Email already exist")
  # Save uploaded files
  image_path = await save_upload_file(image, "images")
  file_path = await save_upload_file(resume_file, "files")
  resume = Resume(
        name=data.name,
        email=data.email,
        dob=data.dob,
        state=data.state,
        gender=data.gender,
        preferred_locations=",".join(data.preferred_locations),
        image_path=image_path,
        resume_file_path=file_path
    )
  session.add(resume)
  await session.commit()
  await session.refresh(resume)
  return resume

async def get_all_resumes(session: AsyncSession):
    resumes = await session.scalars(select(Resume))
    resume_list =  resumes.all()
    for resume in resume_list:
       resume.image_path = get_file_url(resume.image_path)
       resume.resume_file_path = get_file_url(resume.resume_file_path)
    return resume_list
