from fastapi import FastAPI, HTTPException, Depends
from typing import Annotated, List, Optional
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import SessionLocal, engine
from database import engine
from datetime import datetime
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

class Task(TaskBase):
    id: int
    filters: Optional[str] = None
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    cars: List[Car] = []

    class Config:
        orm_mode = True

db_dependency = Annotated[Session, Depends(get_db)]

# POST /tasks
@app.post("/tasks/", response_model = Task)        
def create_tasks(task: TaskBase, db: db_dependency):
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# GET /tasks
@app.get("/tasks/", response_model=List[Task])
def read_tasks(db: db_dependency, skip: int=0, limit: int=100):
    return db.query(models.Task).offset(skip).limit(limit).all()
   

