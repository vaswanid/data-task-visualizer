from fastapi import FastAPI, HTTPException, Depends
from typing import Annotated, List
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine
import models
from database import engine

app = FastAPI()
# install fastapi-cors, import and add CORS middleware

class TaskBase(BaseModel):
    name: str
    description: str
    price: float

class TaskModel(TaskBase):
    id: int
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/tasks/", response_model = TaskModel)        
async def create_tasks(task: TaskBase, db: db_dependency):
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task



@app.get("/tasks/", response_model=List[TaskModel])
async def read_tasks(db: db_dependency, skip: int=0, limit: int=100):
    tasks = db.query(models.Task).offset(skip).limit(limit).all()
    return tasks

