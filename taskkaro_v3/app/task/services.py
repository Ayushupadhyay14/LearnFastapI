from sqlmodel import Session, select
from app.task.models import Task, TaskUpdate, TaskPatch, TaskOut
from fastapi import HTTPException

def create_task(session: Session, new_task: Task) -> TaskOut:
  task = Task(title=new_task.title, content=new_task.content)
  session.add(task)
  session.commit()
  session.refresh(task)
  return task
  
def get_all_tasks(session: Session) -> list[TaskOut]:
    stmt = select(Task)
    tasks = session.exec(stmt)
    return tasks.all()
  
def get_task_by_id(session: Session, task_id: int) -> TaskOut:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
  
def update_task(session: Session, task_id: int, new_task: TaskUpdate) -> TaskOut:

        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        task_data = new_task.model_dump()
        task.sqlmodel_update(task_data)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
    
def patch_task(session: Session, task_id: int, new_task: TaskPatch) -> TaskOut:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task_data = new_task.model_dump(exclude_unset=True)
    task.sqlmodel_update(task_data)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
  
def delete_task(session: Session, task_id: int):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"ok": True}