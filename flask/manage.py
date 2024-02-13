from flask.cli import FlaskGroup
from werkzeug.security import generate_password_hash
from app import app, db
from app.models.authuser import AuthUser
from app.models.userinfo import UserInfo
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
        AuthUser(email="komson@gmail.com",
        name="KK", 
        password=generate_password_hash('1234',
                                method='sha256'))
    )
    # db.session.add(
    #     UserInfo(firstname='สมชาย', lastname='ทรงแบด', email='081-111-1111')
    #     )
    
    db.session.commit()


if __name__ == "__main__":
    cli()