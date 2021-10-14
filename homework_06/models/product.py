from .database import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goods = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
