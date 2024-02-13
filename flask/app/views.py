from flask import (jsonify, render_template,
                   request, url_for, flash, redirect)

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.urls import url_parse

from sqlalchemy.sql import text
from flask_login import login_user

from app import app
from app import db
from app import login_manager
from app.models.authuser import AuthUser

@login_manager.user_loader
def load_user(user_id):
    return AuthUser.query.get(int(user_id))

@app.route('/db')
def db_connection():
# check db connection
    try:
        with db.engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return '<h1>db works.</h1>'
    except Exception as e:
        return '<h1>db is broken.</h1>' + str(e)

@app.route('/')
def firstpage():
    return app.send_static_file("firstpage.html")

@app.route('/signup', methods=("GET", "POST"))
def signup():
    if request.method == 'POST':
        result = request.form.to_dict()
        app.logger.debug(str(result))

        validated = True
        validated_dict = {}
        valid_keys = ['email', 'name', 'password']

        #section 1 validate the input
        for key in result:
            app.logger.debug(str(key)+": " + str(result[key]))
            # screen of unrelated inputs
            if key not in valid_keys:
                continue

            value = result[key].strip()
            if not value or value == 'undefined':
                validated = False
                break
            validated_dict[key] = value
        app.logger.debug("validation done")

        #Section 2 check email and add user to database 
        #if validated still True
        if validated:
            app.logger.debug('validated dict: ' + str(validated_dict))
            email = validated_dict['email']
            name = validated_dict['name']
            password = validated_dict['password']

            #check is email was exists in Database
            user = AuthUser.query.filter_by(email=email).first()
            if user:
                # if email was exists. send user to sign up again

                flash('Email address already exists')
                return redirect(url_for('signup'))
        
        #Section 3 add new user after validated all
        app.logger.debug("preparing to add")
        new_user = AuthUser(email=email, name=name,
                                password=generate_password_hash(
                                    password, method='sha256')
                            )
        #add new_user to database
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return app.send_static_file("signup.html")

@app.route('/login', methods=("GET", "POST"))
def login():
    if request.method == 'POST':    
        # remember = bool(request.form.get('remember'))
        email = request.form.get('email')
        password = request.form.get('password')

        #check is the input email is in databse?
        user = AuthUser.query.filter_by(email=email).first()
        
        #if email not exist in Database or Password Incorrect 
        if not user or not check_password_hash(user.password, password):
            #redirect to give user try again
            return redirect(url_for('login'))
        
        #if user has the right credentials do below
        login_user(user)
        next_page = request.args.get('next')
        #The 'next' parameter is commonly used to redirect users to the page 
        # they were trying to access before being prompted to log in.

        #if user has not expect to go anypage we will set nextpage to homepage
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for("homepage.html")
        return redirect(next_page)

    return app.send_static_file("login.html")


@app.route('/homepage')
def homepage():
    return app.send_static_file("homepage.html")
@app.route('/feedpage')
def feedpage():
    return app.send_static_file("feedpage.html")