from sqlmodel import Session, select
from app.task.models import Task
from app.db.config import engine
from fastapi import HTTPException

def create_task(title: str, content: str):
  task = Task(title=title, content=content)
  with Session(engine) as session:
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
  
def get_all_tasks():
  with Session(engine) as session:
    stmt = select(Task)
    tasks = session.exec(stmt)
    return tasks.all()
  
def get_task_by_id(task_id: int):
  with Session(engine) as session:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
  
def update_task(task_id: int, title: str, content: str):
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        task.title = title
        task.content = content
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
    
def patch_task(task_id: int, title: str | None = None, content: str | None = None):
  with Session(engine) as session:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if title is not None:
        task.title = title
    if content is not None:
        task.content = content
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
  
def delete_task(task_id: int):
  with Session(engine) as session:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return task