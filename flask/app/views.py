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
from flask_login import login_user, login_required, logout_user, current_user
import requests
from datetime import datetime, timezone
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

@app.route('/api')
def board_api():
    # contain all post that didn't hired or deleted
    post_query = PostContent.query.filter_by(is_deleted=False, is_hide=False).order_by(PostContent.created_at).all()
    post = [this_post.to_dict() for this_post in post_query]

    app.logger.debug("board_api: " + str(post))
    hired_post = board_hired().json
    # print("POST", post)
    json_form = jsonify(post)
    return json_form

@app.route('/api/hired')
def board_hired():
    post_query = PostContent.query.all()
    post_hired = []
    for this_post in post_query:
        if this_post.is_hired:
            post_hired.append(this_post.to_dict())

    app.logger.debug("board_api_hired: " + str(post_hired))

    json_form = jsonify(post_hired)
    return json_form

@app.route('/api/deleted')
def board_deleted():
    post_query = PostContent.query.all()
    post_deleted = []
    for this_post in post_query:
        if this_post.is_deleted:
            post_deleted.append(this_post.to_dict())

    app.logger.debug("board_api_deleted: " + str(post_deleted))

    json_form = jsonify(post_deleted)
    return json_form

@app.route('/api/hide')
def board_hid():
    post_query = PostContent.query.all()
    post_hide = []
    for this_post in post_query:
        if this_post.is_hide:
            post_hide.append(this_post.to_dict())

    app.logger.debug("board_api_hide: " + str(post_hide))

    json_form = jsonify(post_hide)
    return json_form

@app.route('/')
def home():
    return app.send_static_file("home.html")

@app.route('/board', methods=("GET", "POST"))
@login_required
def board():
    if request.method == 'POST':
        data = request.form.to_dict()
        app.logger.debug(str(data))
        #the id_post was from html in tag input id=entryid
        #to get which post id in html was we are doing
        id_post = data.get('id', '')
        print("ID-fROM-POST", id_post)
        # this keys are column in database
        valid_keys = ['owner_id','message', 'job_name', 'job_time', 'province',
        'district', 'amphoe', 'zipcode', 'location', 'salary']
        validate_pass = True
        validated_result = {}
        for key in data:
            # screen out an undefined key
            app.logger.debug(str(key) + ": " + str(data[key]))
            if key not in valid_keys:
                continue
            value = data[key].strip() #remove whitespace
            #if caught unexpected value stop validate
            # if not value or value == 'undefined':
            #     validate_pass = False
            #     break
            validated_result[key] = value
        if validate_pass == False:
            app.logger.debug("===== Validation Fail ;-; =====")

        if validate_pass:
            app.logger.debug("===== validation Complete 100% =====")
            app.logger.debug("===== Trying to add data into database =====")
            app.logger.debug("validated result: " + str(validated_result))
            owner_id = validated_result['owner_id']
            # user = Member.query.filter_by(owner_email=owner_email).first()
            if not id_post:
                app.logger.debug("===== new post DETECTED =====")
                # this post was created for first time
                # print("IDPOST", id_post)
                validated_result['owner_id'] = current_user.id
                new_post = PostContent(**validated_result)
                app.logger.debug(str(new_post))
                db.session.add(new_post)
            else:
                app.logger.debug("===== old post DETECTED =====")
                #this post already created then update this post
                #prevent edited in backend level
                print("POST ID", id_post)
                print("OWNER", owner_id)
                owner_post = PostContent.query.get(id_post)
                if owner_post.owner_id == current_user.id:
                    owner_post.update(**validated_result)
                app.logger.debug("===== update COMPLETE 100% =====")
            db.session.commit()
    post = board_api().json
    post = list(reversed(post))
    return render_template("board.html",allpost=post)

@app.route('/board/delete', methods=('GET', 'POST'))
def board_delete():
    app.logger.debug("===== DELETE FUNCTION =====")
    if request.method == 'POST':
        result = request.form.to_dict()
        id_ = result.get('id', '')
        try:
            #if now user is owner of this post
            post = PostContent.query.get(id_)
            if post.owner_id == current_user.id or current_user.id == 1:
                post.is_deleted = True
                post.deleted_at = datetime.now(timezone.utc)
                post.delete_by = current_user.id
                db.session.commit()

            if  post.is_deleted:
                print("Post has been successfully marked as deleted.")
            else:
                print("Failed to mark post as deleted.")
        except Exception as ex:
           app.logger.error(f"Error removing post with id {id_}: {ex}")
           raise
    return (board_api())

@app.route('/board/undelete', methods=('GET', 'POST'))
def board_undelete():
    app.logger.debug("===== UNDELETE FUNCTION =====")
    if request.method == 'POST':
        result = request.form.to_dict()
        id_ = result.get('id', '')
        try:
            #if now user is owner of this post
            post = PostContent.query.get(id_)
            if post.owner_id == current_user.id or current_user.id == 1:
                post.is_deleted = False
                post.deleted_at = None
                post.delete_by = None
                db.session.commit()

            if not post.is_deleted:
                print("Post has been successfully unmarked from deleted.")
            else:
                print("Failed to unmark post from deleted.")
        except Exception as ex:
           app.logger.error(f"Error unremoving post with id {id_}: {ex}")
           raise
    return board_api()

@app.route('/board/hired', methods=('GET', 'POST'))
def board_hire():

    app.logger.debug("===== HIRED FUNCTION =====")
    if request.method == 'POST':
        result = request.form.to_dict()
        id_ = result.get('id', '')
        try:
            #if now user is owner of this post
            post = PostContent.query.get(id_)
            if post.owner_id == current_user.id:
                post.is_hired = True
                post.hired_at = datetime.now(timezone.utc)
                db.session.commit()

            if  post.is_deleted:
                print("Post has been successfully marked as hired.")
            else:
                print("Failed to mark Post as hired.")
        except Exception as ex:
           app.logger.error(f"Error mark post as hried with id {id_}: {ex}")
           raise
    return board_api()

# @app.route('/board/hide', methods=('GET', 'POST'))
# def board_hide():
#     app.logger.debug("===== HIDE FUNCTION =====")
#     if request.method == 'POST':
#         result = request.form.to_dict()
#         #get the post_id
#         id_ = result.get('id', '')
#         try:
#             #if now user is admin
#             post = PostContent.query.get(id_)
#             if current_user.id == 1:
#                 post.is_hide = True
#                 post.hide_at = datetime.now(timezone.utc)
#                 db.session.commit()

#             if  post.is_hide:
#                 print("Post has been successfully marked as hide.")
#             else:
#                 print("Failed to mark Post as hide.")
#         except Exception as ex:
#            app.logger.error(f"Error mark post as hide with id {id_}: {ex}")
#            raise
#     return board_api()

# @app.route('/board/unhide', methods=('GET', 'POST'))
# def board_unhide():
    app.logger.debug("===== UNHIDE FUNCTION =====")
    if request.method == 'POST':
        result = request.form.to_dict()
        #get the post_id
        id_ = result.get('id', '')
        try:
            #if now user is admin
            post = PostContent.query.get(id_)
            if current_user.id == 1:
                post.is_hide = False
                post.hide_at = None
                db.session.commit()

            if  post.is_hide:
                print("Post has been successfully unmarked from hide.")
            else:
                print("Failed to unmark Post from hide.")
        except Exception as ex:
           app.logger.error(f"Error unmark post from hide with id {id_}: {ex}")
           raise
    return board_api()

@app.route('/profile')
@login_required
def profile():
    query = (PostContent.query.filter_by(owner_id=current_user.id,is_deleted=False)
    .order_by(PostContent.created_at.desc()))
    user_post = [this_post.to_dict() for this_post in query]
    
    return render_template("profile.html",user_post=user_post)

@app.route('/oprofile', methods=('GET', 'POST'))
def oprofile():

    if request.method == 'POST':
        result = request.form.to_dict()
        owner = result.get('id', '')
        post_query = PostContent.query.filter_by(owner_id=owner,is_deleted=False, is_hide=False).order_by(PostContent.created_at).all()
        owner_post = [this_post.to_dict() for this_post in post_query]
        print(owner_post)
        user = Member.query.get(owner)
        user_name = user.name
        user_email =user.email
        user_avatar = user.avatar_url
        user_describe = user.about_me
        return render_template('oprofile.html',owner_post=owner_post,
        owner_name=user_name,owner_email=user_email,
        owner_avatar=user_avatar,owner_aboutme=user_describe)
    else:  # Handle the GET request
        # You might want to redirect to another page or return an error response
        return "Invalid request"

@app.route('/describe',methods=('GET', 'POST'))
def describe():
    if request.method == 'POST':
        result = request.form.to_dict()
        owner = result.get('owner_id', '')
        about_me = result.get('descript','')
        user = Member.query.get(owner)
        user.about_me = about_me
        db.session.commit()
        return board_api()
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

                # flash('Email address already exists')
                return redirect(url_for('signup'))
            elif password != cfpassword:
                # flash("password doesn't match")
                return redirect(url_for('signup'))
        #Section 3 add new user after validated all
        app.logger.debug("preparing to add")
        avatar_url = gen_avatar_url(email, name)
        new_user = Member(email=email, name=name,
                                password=generate_password_hash(
                                    password, method='sha256'),
                                avatar_url=avatar_url,
                                login_type='hirethec'
                            )
        #add new_user to database
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return app.send_static_file("signup.html")
@app.route('/logout')
@login_required
def logout():
    user = Member.query.get(current_user.id)
    # type_login = user.login_type
    # print("ACTK", user.user_token)
    # print("TK",tk)
    # print("TYPELOGIN", type_login)

    # revoke for unbond account from google
    
    logout_user()
    return redirect(url_for('home'))

@app.route('/google/revoke', methods=['POST'])
def google_revoke(token):
    response = requests.post('https://oauth2.googleapis.com/revoke',
    params={'token': token},
    headers = {'content-type': 'application/x-www-form-urlencoded'})
    if response.status_code == 200:
        print("Token successfully revoked")
    else:
        print("Failed to revoke token")
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
        avatar_url= gen_avatar_url(email, name)
        new_user = Member(email=email, name=name,
                           password=generate_password_hash(
                               password, method='sha256'),
                            avatar_url=avatar_url,
                            login_type='google'
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
        avatar_url= gen_avatar_url(email, name)
        new_user = Member(email=email, name=name,
                           password=generate_password_hash(
                               password, method='sha256'),
                            avatar_url=avatar_url,
                            login_type='github'
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
        avatar_url= gen_avatar_url(email, name)
        new_user = Member(email=email, name=name,
                           password=generate_password_hash(
                               password, method='sha256'),
                            avatar_url=avatar_url
                           )
        db.session.add(new_user)
        db.session.commit()
        user = Member.query.filter_by(email=email).first()
    login_user(user)
    return redirect('/board')

def gen_avatar_url(email, name):
    bgcolor = generate_password_hash(email, method="sha256")[-6:]
    color = hex(int("0xffffff", 0) - int("0x" + bgcolor, 0)).replace("0x", "")
    lname = ""
    temp = name.split()
    fname = temp[0][0]
    if len(temp) > 1:
        lname = temp[1][0]

    avatar_url = (
        "https://ui-avatars.com/api/?name="
        + fname
        + "+"
        + lname
        + "&background="
        + bgcolor
        + "&color="
        + color
    )
    return avatar_url