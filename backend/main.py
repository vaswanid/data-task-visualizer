from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from . import models
from .database import SessionLocal, engine
from .models import Task, Car
from . import task_queue
from typing import Optional, List, Annotated
from fastapi.responses import FileResponse
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import asyncio
import os
from fastapi import HTTPException


app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def serve_home():
    return FileResponse("frontend/index.html")

templates = Jinja2Templates(directory="templates")

from fastapi.middleware.cors import CORSMiddleware
# Enable CORS (important for frontend communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
models.Base.metadata.create_all(bind=engine)

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class CarBase(BaseModel):
    car_company: str
    car_model: str
    date_of_sale: datetime
    price: float
    discount: float
    warranty_years: int
    is_new: bool
    mileage: float

class CarCreate(CarBase):
    pass

class Car(CarBase):
    id: int
    class Config:
        orm_mode = True

class TaskBase(BaseModel):
    filters: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    status: Optional[str] = None

class TaskDelete(TaskBase):
    status: Optional[str] = None

class Task(TaskBase):
    id: int
    filters: Optional[str] = None
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    cars: List[Car] = []

    class Config:
        orm_mode = True

class TaskCreateResponse(BaseModel):
    message : str
    tasks : Task 
     
db_dependency = Annotated[Session, Depends(get_db)]

from fastapi import APIRouter
from fastapi.responses import JSONResponse

@app.get("/cars")
def get_all_cars(db: Session = Depends(get_db)):
    return db.query(models.Car).all()

@app.get("/tasks/{task_id}/cars")
def get_task_cars(task_id: int, db: Session = Depends(get_db)):
    return db.query(models.Car).filter(models.Car.task_id == task_id).all()

@app.on_event("startup")
async def start_background_tasks():
    asyncio.create_task(task_queue.process_tasks())

# CREATE =
# POST /tasks
@app.post("/tasks/", response_model = Task)        
async def create_tasks(task: TaskBase, db: db_dependency):
    db_task = models.Task(
        filters = task.filters,
        status = "Pending",
        created_at = datetime.utcnow()
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    await task_queue.put((db_task.id, task.filters))  # send to job queue for processing
    
    return {
        "message": "Task created successfully",
        "task": db_task
    }

# READ =
# GET /tasks (all)
@app.get("/tasks/", response_model=List[Task])
def read_tasks(db: db_dependency, skip: int=0, limit: int=100):
    return db.query(models.Task).offset(skip).limit(limit).all()

# GET /tasks/{task_id} (single task with cars)
@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int, db: db_dependency):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# GET /tasks/{task_id}/cars (only related cars)
@app.get("/tasks/{task_id}/cars", response_model=List[Car])
def get_task_cars(task_id: int, db: db_dependency):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task.cars

#UPDATE =
# PUT /tasks/{task_id}
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskUpdate, db: db_dependency):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task_update.filters is not None:
        task.filters = task_update.filters
    if task_update.status is not None:
        task.status = task_update.status
    db.commit()
    db.refresh(task)
    return task

#DELETE  /tasks/{task_id}
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: db_dependency):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}

@app.on_event("startup")
async def start_background_tasks():
    asyncio.create_task(task_queue.process_tasks())




