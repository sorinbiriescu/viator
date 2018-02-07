import os

import requests
from flask import (Blueprint, jsonify, redirect, render_template, request,
                   url_for)
from flask_login import login_required, login_user, logout_user

from app.forms.forms_main import (LoginForm, PoiTypeForm, RouteForm,
                                  SearchForm, SignupForm)
from app.models.models_user import User

script_dir = os.path.dirname(__file__)

main = Blueprint('main', __name__)


@main.route('/explore', methods=['GET'])
@login_required
def explore():
    return render_template('/main/explore.html')


@main.route('/itinerary/<id>', methods=['GET'])
@login_required
def itinerary():
    return render_template('/main/itinerary.html')


@main.route('/user_dashboard/<user>', methods=['GET'])
@login_required
def user_dashboard(user):
    user = User.get_user(user)
    content = {
        "user": user
    }

    return render_template('/main/user_dashboard.html', **content)


@main.route('/signup', methods=['GET', 'POST'])
def register():
    form = SignupForm()

    if request.method == 'GET':
        return render_template('/main/signup.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            if User.get_user(email=form.email.data):
                return 'Email already exists in database'
            else:
                new_user = User.add_user_to_db(
                    email=form.email.data, password=form.password.data)
                login_user(new_user)

                return 'User created'
    else:
        'Form error'


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'GET':
        return render_template('/main/login.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            user = User.get_user(email=form.email.data)
            if user:
                if user.password == form.password.data:
                    login_user(user)
                    return redirect(
                        request.args.get('next')
                        or url_for('main.user_dashboard', user=user.email))
            else:
                return "User does not exist"
    else:
        return "Form error"


@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
