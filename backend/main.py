from fastapi import FastAPI, HTTPException, Depends
from typing import Annotated, List
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import SessionLocal, engine
from database import engine
import models

# Initialize app
app = FastAPI()

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

class TaskBase(BaseModel):
    name: str
    description: str
    price: float

class TaskCreate(TaskBase):
    pass

class TaskModel(TaskBase):
    id: int
    class Config:
        orm_mode = True

db_dependency = Annotated[Session, Depends(get_db)]

# POST /tasks
@app.post("/tasks/", response_model = TaskModel)        
def create_tasks(task: TaskBase, db: db_dependency):
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# GET /tasks
@app.get("/tasks/", response_model=List[TaskModel])
def read_tasks(db: db_dependency, skip: int=0, limit: int=100):
    return db.query(models.Task).offset(skip).limit(limit).all()
   

