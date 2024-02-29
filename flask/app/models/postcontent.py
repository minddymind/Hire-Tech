# Komson 
#ยังไม่เสร็จ
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from app import db


class UserInfo(db.Model):

    __tablename__ = "post_content"

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    email = db.Column(db.String(20))

    def __init__(self, firstname, lastname, email):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email