from pydantic import BaseModel, EmailStr
from datetime import date
from typing import List
from enum import Enum

class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"

class ResumeCreate(BaseModel):
    name: str
    email: EmailStr
    dob: date
    state: str
    gender: GenderEnum
    preferred_locations: List[str]

class ResumeOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    dob: date
    state: str
    gender: GenderEnum
    preferred_locations: str
    image_path: str
    resume_file_path: str
    model_config = {
        "from_attributes": True
        }