from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Date
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    filters = Column(Text)
    status = Column(String(64), default='pending')
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    cars = relationship('Car', back_populates='task')

class Car(Base):
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))

    car_company = Column(String(64), index=True)
    car_model = Column(String(64), index=True)
    date_of_sale = Column(Date, index=True)
    price = Column(Float)
    discount = Column(Float)
    warranty_years = Column(Integer)
    is_new = Column(Boolean)
    mileage = Column(Float)

    task = relationship('Task', back_populates='cars')
