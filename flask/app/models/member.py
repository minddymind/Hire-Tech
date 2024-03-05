# Komson 
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
from app import db

#user that already in Database (Member)
class Member(db.Model, UserMixin):
    __tablename__ = "members"
    # primary keys are required by SQLAlchemy

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(1000))
    password = db.Column(db.String(100))
    avatar_url = db.Column(db.String(100))
    login_type = db.Column(db.String)
    about_me = db.Column(db.String)
    # user_token = db.Column(MutableDict.as_mutable(JSONB))

    def __init__(self, email, name, password, login_type, avatar_url):
        self.email = email
        self.name = name
        self.password = password
        self.login_type = login_type
        self.avatar_url = avatar_url

    def update(self, update_email, update_name, update_password,
    update_avatar_url,login_type=None):
        self.email = update_email
        self.name = update_name
        self.password = update_password       
        self.avatar_url = update_avatar_url
        self.login_type = login_type
