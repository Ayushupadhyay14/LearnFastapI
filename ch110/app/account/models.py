from beanie import Document
from pydantic import Field

class User(Document):
    name: str = Field(..., max_length=50)
    email: str = Field(..., max_length=255)

    class Settings:
        name = "users"
