# Komson 
#ยังไม่เสร็จ
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime, timezone
from .member import Member
from app import db

class PostContent(db.Model, SerializerMixin):
    __tablename__ = "post_content"
    #init in this class
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(1000))
    job_name = db.Column(db.String(100))
    job_time = db.Column(db.String(100))
    province = db.Column(db.String(100))
    district = db.Column(db.String(100), default=None)
    amphoe = db.Column(db.String(100), default=None)
    zipcode = db.Column(db.String(100), default=None)
    location = db.Column(db.String(100), default=None) 
    salary = db.Column(db.String, default=None)
    #FK of member
    owner_id = db.Column(db.Integer, db.ForeignKey("members.id"))  
    owner_name = db.Column(db.String(1000))
    owner_email = db.Column(db.String(100))
    owner_avatar = db.Column(db.String(100))
    #time server
    created_at = db.Column(db.DateTime())
    edited_at = db.Column(db.DateTime())
    hired_at = db.Column(db.DateTime())
    deleted_at = db.Column(db.DateTime())
    hide_at = db.Column(db.DateTime())
    #functional
    is_deleted = db.Column(db.Boolean, default=False)
    delete_by = db.Column(db.Integer, default=None)
    is_hired = db.Column(db.Boolean, default=False)
    is_hide = db.Column(db.Boolean, default=False)

    def __init__(self, owner_id, job_time=None,
    job_name=None, message=None,province=None, salary=None, district=None, amphoe=None, zipcode=None, 
    location=None):
        # print("OWERNID",owner_id)   
        # print("OWNERID", self.owner_id)

        self.owner_id = owner_id
        owner = Member.query.get(self.owner_id)

        # check is this post have owner and set value of this
        #  post related to owner
        if owner:
            owner_email = owner.email 
            owner_name = owner.name
            owner_avatar = owner.avatar_url
        else:
            owner_email = None
            owner_name = None
            owner_avatar = None

        self.owner_name = owner_name
        self.owner_email = owner_email
        self.job_time = job_time
        self.job_name = job_name
        self.message = message
        self.province = province
        self.district = district
        self.amphoe = amphoe
        self.zipcode = zipcode
        self.location = location
        self.salary = salary

        self.owner_avatar = owner_avatar
        self.created_at = datetime.now(timezone.utc)
        
    def update(self, owner_id, job_time,
    job_name, message,province, salary, district=None, amphoe=None, zipcode=None, 
    location=None):
        # check is this post have owner and set value of this
        #  post related to owner
        owner = Member.query.get(self.owner_id)
        if owner:
            email = owner.email 
            name = owner.name    
        self.owner_name = name
        self.owner_email = email
        self.job_time = job_time
        self.job_name = job_name
        self.message = message
        self.province = province
        self.district = district
        self.amphoe = amphoe
        self.zipcode = zipcode
        self.location = location
        self.salary = salary
        self.edited_at = datetime.now(timezone.utc)



