import os
import json
import secrets
import string
# Komson 
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
import authlib.integrations.base_client
from app import oauth
from app.models.member import Member
from app.models.postcontent import PostContent
@login_manager.user_loader
def load_user(user_id):
    return Member.query.get(int(user_id))

@app.route('/')
def home():
    return app.send_static_file("home.html")

@app.route('/board')
@login_required
def board():
    return render_template("board.html")

@app.route('/profile')
def profile():
    return render_template("profile.html")

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
        
        email = request.form.get("email")
        password = request.form.get("password")
        print(email, password)
        #check is the input email is in databse?
        user = Member.query.filter_by(email=email).first()
        
        #if email not exist in Database or Password Incorrect 
        if not user or not check_password_hash(user.password, password):
            print('redirect to give user try again')
            return redirect(url_for('login'))
        
        #if user has the right credentials do below
        login_user(user)
        next_page = request.args.get('next')
        #The 'next' parameter is commonly used to redirect users to the page 
        # they were trying to access before being prompted to log in.

        #if user has not expect to go anypage we will set nextpage to home
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for("board")
        return redirect(next_page)

    return app.send_static_file("login.html")

@app.route('/signup', methods=("GET", "POST"))
def signup():
    if request.method == 'POST':
        result = request.form.to_dict()
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
            user = Member.query.filter_by(email=email).first()
            if user:
                # if email was exists. send user to sign up again

                flash('Email address already exists')
                return redirect(url_for('signup'))
            elif password != cfpassword:
                flash("password doesn't match")
                return redirect(url_for('signup'))
        #Section 3 add new user after validated all
        app.logger.debug("preparing to add")
        new_user = Member(email=email, name=name,
                                password=generate_password_hash(
                                    password, method='sha256')
                            )
        #add new_user to database
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return app.send_static_file("signup.html")
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

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
    try:
        token = oauth.google.authorize_access_token()
    except authlib.integrations.base_client.errors.OAuthError:
        return redirect(url_for('login'))
    app.logger.debug(str(token))
    
    userinfo = token['userinfo']
    app.logger.debug(" Google User " + str(userinfo))
    email = userinfo['email']
    user = Member.query.filter_by(email=email).first()

    if not user:
        name = userinfo.get('given_name','') + " " + userinfo.get('family_name','')
        random_pass_len = 8
        password = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                          for i in range(random_pass_len))
        picture = userinfo['picture']
        new_user = Member(email=email, name=name,
                           password=generate_password_hash(
                               password, method='sha256')
                           )
        db.session.add(new_user)
        db.session.commit()
        user = Member.query.filter_by(email=email).first()
    login_user(user)
    return redirect('/board')

github = oauth.register(
    name='github',
    client_id=app.config['GITHUB_CLIENT_ID'],
    client_secret=app.config['GITHUB_CLIENT_SECRET'],
    access_token_url="https://github.com/login/oauth/access_token",
    access_token_params=None,
    authorize_url="https://github.com/login/oauth/authorize",
    authorize_params=None,
    api_base_url="https://api.github.com/",
    client_kwargs={
        'scope': 'user:email'}
)
@app.route('/github/')
def github_login():
    redirect_uri = url_for('github_auth', _external=True)
    return github.authorize_redirect(redirect_uri)

@app.route('/github/auth')
def github_auth():
    try :
        token = github.authorize_access_token()
    except authlib.integrations.base_client.errors.OAuthError:
        return redirect(url_for('login'))
    gh_resp = github.get('user').json()
    print("**resp", gh_resp)
    
    app.logger.debug(" Github User " , gh_resp)
    email = gh_resp['email']
    name = gh_resp['login']
    if email == None:
        email = name
    print(email)

    user = Member.query.filter_by(email=email).first()

    if not user:
        random_pass_len = 8
        password = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
        for i in range(random_pass_len))
        # picture = userinfo['picture']
        new_user = Member(email=email, name=name,
                           password=generate_password_hash(
                               password, method='sha256')
                           )
        db.session.add(new_user)
        db.session.commit()
        user = Member.query.filter_by(email=email).first()
    login_user(user)
    return redirect('/board')

@app.route('/facebook/')
def facebook_login():
    facebook = oauth.register(
        name='facebook',
        client_id=app.config['FACEBOOK_CLIENT_ID'],
        client_secret=app.config['FACEBOOK_CLIENT_SECRET'],
        access_token_url='https://graph.facebook.com/oauth/access_token',
        access_token_params=None,
        authorize_url='https://www.facebook.com/dialog/oauth',
# base_url = "https://www.facebook.com/v13.0/dialog/oauth"
        authorize_params=None,
        api_base_url='https://graph.facebook.com/',
        client_kwargs={'scope': 'email'},
    )
    redirect_uri = url_for('facebook_auth', _external=True)
    return oauth.facebook.authorize_redirect(redirect_uri)

@app.route('/facebook/auth')
def facebook_auth():
    try:
        token = oauth.facebook.authorize_access_token()
    except authlib.integrations.base_client.errors.OAuthError:
        return redirect(url_for('login'))
    resp = oauth.facebook.get(
    'https://graph.facebook.com/me?fields=id,name,email,picture{url}')
    
    fb_profile = resp.json()
    print("Facebook User ", fb_profile)
    
    app.logger.debug(" Facebook User " , fb_profile)
    email = fb_profile['email']
    user = Member.query.filter_by(email=email).first()

    if not user:
        name = fb_profile['name']
        random_pass_len = 8
        password = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
        for i in range(random_pass_len))
        # picture = userinfo['picture']
        new_user = Member(email=email, name=name,
                           password=generate_password_hash(
                               password, method='sha256')
                           )
        db.session.add(new_user)
        db.session.commit()
        user = Member.query.filter_by(email=email).first()
    login_user(user)
    return redirect('/board')

