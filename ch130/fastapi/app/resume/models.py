from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text
from app.db.config import Base
import enum
from datetime import date

class GenderEnum(str, enum.Enum):
    male = "male"
    female = "female"
    other = "other"

class Resume(Base):
    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    dob: Mapped[date]
    state: Mapped[str] = mapped_column(String(200))
    gender: Mapped[GenderEnum]
    preferred_locations: Mapped[str] = mapped_column(Text)
    image_path: Mapped[str] = mapped_column(String(255))
    resume_file_path: Mapped[str] = mapped_column(String(255))



