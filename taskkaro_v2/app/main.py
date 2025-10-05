from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.config import create_tables
from app.task.services import *
from app.task.models import TaskCreate, TaskUpdate, TaskPatch, TaskOut
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()  
    yield 

app = FastAPI(lifespan=lifespan)

@app.post("/task", response_model=TaskOut)
def task_create(new_task: TaskCreate):
   task = create_task(new_task)
   return task

@app.get("/tasks", response_model=list[TaskOut])
def all_tasks():
  tasks = get_all_tasks()
  return tasks

@app.get("/task/{task_id}", response_model=TaskOut)
def get_task(task_id: int):
    task = get_task_by_id(task_id)
    return task

@app.put("/task/{task_id}", response_model=TaskOut)
def put_task(task_id: int, new_task: TaskUpdate):
    task = update_task(task_id, new_task)
    return task

@app.patch("/task/{task_id}", response_model=TaskOut)
def task_patch(task_id: int, new_task: TaskPatch):
    task = patch_task(task_id, new_task)
    return task

@app.delete("/task/{task_id}")
def task_delete(task_id: int):
    task = delete_task(task_id)
    return task