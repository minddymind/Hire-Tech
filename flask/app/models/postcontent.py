# Komson 
#ยังไม่เสร็จ
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from models.memer import Member
from app import db


class PostContent(db.Model):
    __tablename__ = "post_content"
    
    post_id = db.Column(db.Integer, primary_key=True)
    owner_name = db.Column(db.String(1000))
    owner_email = db.Column(db.String(100))
    job = db.Column(db.String)
    message = db.Column(db.String)
    province = db.Column(db.String)  

    owner_id = db.Column(db.Integer, db.ForeignKey("members.id"))  

    def __init__(self, owner_name, owner_email, job):
        # check is this post have owner and set value of this post to owner
        owner = Member.query.get(self.owner_id)
        if owner:
            email = owner.email 
            name = owner.name

        self.owner_name = owner_name
        self.owner_email = owner_email
        self.job = job