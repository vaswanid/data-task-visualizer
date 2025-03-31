from backend import db

class Car(db.model):
    __tablename__ = 'Car'
    id = db.Column(db.Integer, primary_key = True)
    Car_company = db.Column(db.String(64), unique=True, index = True)
    Car_model = db.Column(db.String(64), unique=True, index = True)
    date_of_sale = db.Column(db.Date, unique=True, index = True




