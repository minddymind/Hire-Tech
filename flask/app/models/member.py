# Komson 
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from app import db

#user that already in Database (Member)
class Member(db.Model, UserMixin):
    __tablename__ = "members"
    # primary keys are required by SQLAlchemy

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(1000))
    password = db.Column(db.String(100))

    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password
        
    def update(self, update_email, update_name, update_password):
        self.email = update_email
        self.name = update_name
        self.password = update_password       
