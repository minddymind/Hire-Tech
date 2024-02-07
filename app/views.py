import json
from flask import (jsonify, render_template,
                   request, url_for, flash, redirect)
from app import app
# from app.forms import forms

@app.route('/')
def homepage():
    return app.send_static_file("homepage.html")