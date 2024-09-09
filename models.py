from database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False , unique=True)
    password = db.Column(db.String(100), nullable=False)
    secret= db.Column(db.String(32), nullable=False)
    is_admin= db.Column(db.Boolean(), nullable=False)