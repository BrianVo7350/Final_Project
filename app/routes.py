from flask import render_template, request, flash, redirect, url_for
from app import app
from forms import Pokemon_search
import requests
from .models import User, db
from flask_login import login_required, current_user


@app.route('/')
def home_page():
    return render_template('index.html')

# @app.route('/')
# def home_page():
#     return render_template('index.html')

# @app.route('/')
# def home_page():
#     return render_template('index.html')