from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from backend import db


class Task(db.model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    filters = db.Column(db.Text)  # Use Text to allow large filter JSON
    status = db.Column(db.String(64), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)

    # Relationship with Car (aka Record)
    cars = db.relationship('Car', back_populates='tasks', lazy=True)

class Car(db.model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key = True)

    # Foreign key to Task table
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"))

     # Car details
    car_company = db.Column(db.String(64), index = True)
    car_model = db.Column(db.String(64), index = True)
    date_of_sale = db.Column(db.Date, index = True)
    price = db.Column(db.Float)
    discount = db.Column(db.Float)
    warranty_years = db.Column(db.Integer)
    is_new = db.Column(db.Boolean)
    mileage = db.Column(db.Float)
    # Relationship back to Task model
    task = db.relationship('Task', back_populates='cars')



