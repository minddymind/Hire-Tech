import json
from flask import (jsonify, render_template,
                   request, url_for, flash, redirect)

from sqlalchemy.sql import text
from app import app
from app import db

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

@app.route('/signup')
def signup():
    return app.send_static_file("signup.html")

@app.route('/login')
def login():
    return app.send_static_file("login.html")

@app.route('/feedpage')
def feedpage():
    return app.send_static_file("feedpage.html")