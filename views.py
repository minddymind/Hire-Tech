import json
from flask import (jsonify, render_template,
                   request, url_for, flash, redirect)
from app import app
from app.forms import forms

@app.route('/')
