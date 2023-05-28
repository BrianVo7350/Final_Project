from flask import render_template, request, flash, redirect, url_for, Blueprint
from .forms import Signup, Login
import requests
from ..models import User
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ["GET", "POST"])
def signup():
    form = Signup()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            user = User.query.filter_by(username = username).first()
            if user:
                flash('That username is taken.', 'danger')
                return render_template('signup.html', form = form, usernameError = True)
            user = User.query.filter_by(email = email).first()
            if user:
                flash('That email is already in use. Please use another email.', 'danger')
                return render_template('signup.html', form = form, emailError=True)
            user = User(username, email, password)
            user.saveToDB()
            flash('Successfully created your account.', 'success')
            return redirect(url_for('auth.login_page'))
        else:
            flash('Invalid entry. Please try again', 'danger')
    return render_template('signup.html', form = form)
    

@auth.route('/login', methods = ["POST", "GET"])
def login_page():
    form = Login()
    if request.method == 'POST':
         if form.validate():
            username = form.username.data
            password = form.password.data

            user = User.query.filter_by(username = username).first()
            if user:
                if user.password == password:
                    login_user(user)
                    return redirect(url_for('home_page'))
                else:
                    flash('invalid password')
            else:
                flash('incorrect username or password')

            return render_template('login.html', form = form)
    return render_template('login.html', form = form)
         
 
@auth.route('/logout')
@login_required
def logMeOut():
    logout_user()
    return redirect(url_for('auth.login_page'))