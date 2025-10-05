from sqlmodel import Field, SQLModel

class TaskBase(SQLModel):
    title: str
    content: str

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class TaskPatch(SQLModel):
    title: str | None = None
    content: str | None = None

class TaskOut(TaskBase):
    id: int
    
class Task(TaskBase, table=True):
    id: int = Field(primary_key=True)