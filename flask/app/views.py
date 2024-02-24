import json
import secrets
import string
from flask import (jsonify, render_template,
                   request, url_for, flash, redirect)

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.urls import url_parse

from sqlalchemy.sql import text
from flask_login import login_user, login_required, logout_user
import requests
from app import app
from app import db
from app import login_manager
from app import oauth
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


@app.route('/login', methods=("GET", "POST"))
def login():
    if request.method == 'POST':    
        # remember = bool(request.form.get('remember'))
        body = request.get_json()
        email = body['email']
        password = body['password']

        #check is the input email is in databse?
        user = AuthUser.query.filter_by(email=email).first()
        
        #if email not exist in Database or Password Incorrect 
        if not user or not check_password_hash(user.password, password):
            #redirect to give user try again
            return jsonify({'path':url_for('login')})
        
        #if user has the right credentials do below
        login_user(user)
        next_page = request.args.get('next')
        #The 'next' parameter is commonly used to redirect users to the page 
        # they were trying to access before being prompted to log in.

        #if user has not expect to go anypage we will set nextpage to home
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for("home")
        return jsonify({'path':next_page})

    return app.send_static_file("login.html")

@app.route('/signup', methods=("GET", "POST"))
def signup():
    if request.method == 'POST':
        result = request.get_json()
        app.logger.debug(str(result))

        validated = True
        validated_dict = {}
        valid_keys = ['email', 'name', 'password', 'cfpassword']

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
            cfpassword = validated_dict['cfpassword']
            #check is email was exists in Database
            user = AuthUser.query.filter_by(email=email).first()
            if user:
                # if email was exists. send user to sign up again

                flash('Email address already exists')
                return jsonify({'path':url_for('signup')})

        #Section 3 add new user after validated all
        app.logger.debug("preparing to add")
        new_user = AuthUser(email=email, name=name,
                                password=generate_password_hash(
                                    password, method='sha256')
                            )
        #add new_user to database
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'path':url_for("login")})
    return app.send_static_file("signup.html")


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@app.route('/googleapi')
def get_google_provider_cfg():
    return requests.get(app.config['GOOGLE_DISCOVERY_URL']).json()



@app.route('/google/')
def google():
    oauth.register(
        name='google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        server_metadata_url=app.config['GOOGLE_DISCOVERY_URL'],
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
    
   # Redirect to google_auth function
    redirect_uri = url_for('google_auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/google/auth/')
def google_auth():
    token = oauth.google.authorize_access_token()
    app.logger.debug(str(token))
    
    userinfo = token['userinfo']
    app.logger.debug(" Google User " + str(userinfo))
    email = userinfo['email']
    user = AuthUser.query.filter_by(email=email).first()

    if not user:
        name = userinfo.get('given_name','') + " " + userinfo.get('family_name','')
        random_pass_len = 8
        password = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                          for i in range(random_pass_len))
        picture = userinfo['picture']
        new_user = AuthUser(email=email, name=name,
                           password=generate_password_hash(
                               password, method='sha256')
                           )
        db.session.add(new_user)
        db.session.commit()
        user = AuthUser.query.filter_by(email=email).first()
    login_user(user)
    return redirect('/home')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
    

@app.route('/')
def home():
    return app.send_static_file("home.html")


@app.route('/board')
# @login_required
def board():
    return app.send_static_file("board.html")

