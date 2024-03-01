# Komson 
from flask.cli import FlaskGroup
from werkzeug.security import generate_password_hash
from app import app, db
from app.models.member import Member
from app.models.postcontent import PostContent
cli = FlaskGroup(app)

#create DB
@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

#
@cli.command("seed_db")
def seed_db():
    db.session.add(
        Member(email="admin@1234",
        name="admin", 
        password=generate_password_hash('1234',
                                method='sha256'))
    )
    db.session.commit()
    db.session.add(
        PostContent(message='ประกาศรับสมัครงานจากแอดมินจ้า',
        job_name='Full-Stack-Developer',
        job_time='Full-time',
        province='Chiang Mai',
        amphoe='Muaing',
        location='บริเวณมหาวิทยาลัยเชียงใหม่',
        salary=90000,
        owner_id=1
        )
    )
    db.session.commit()
    test_delete()
    
def test_update():
    post = PostContent.query.get(1)
    update_post = {'message':'ประกาศรับสมัครงานจากแอดมินจ้า EDIT',
        'job_name':'Full-Stack-Developer',
        'job_time':'Full-time',
        'province':'Chiang Mai',
        'amphoe':'Muang',
        'location':'บริเวณมหาวิทยาลัยเชียงใหม่',
        'salary':90000,
        'owner_id':1
    }
    
    post.update(**update_post)
    db.session.commit()

def test_hired():
    post = PostContent.query.get(1)
    update_post = {'message':'ประกาศรับสมัครงานจากแอดมินจ้า HIRED',
        'job_name':'Full-Stack-Developer',
        'job_time':'Full-time',
        'province':'Chiang Mai',
        'amphoe':'Muang',
        'location':'บริเวณมหาวิทยาลัยเชียงใหม่',
        'salary':90000,
        'owner_id':1
    }
    
    post.hired(**update_post)
    db.session.commit()
def test_delete():
    post = PostContent.query.get(1)
    update_post = {'message':'ประกาศรับสมัครงานจากแอดมินจ้า DEL',
        'job_name':'Full-Stack-Developer',
        'job_time':'Full-time',
        'province':'Chiang Mai',
        'amphoe':'Muang',
        'location':'บริเวณมหาวิทยาลัยเชียงใหม่',
        'salary': 90000,
        'owner_id':1
    }
    
    post.deleted(**update_post)
    db.session.commit()
if __name__ == "__main__":
    cli()