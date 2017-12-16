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

mapzen_api = 'mapzen-fPCfu1G'


@main.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm(request.form)
    if request.method == 'POST' and form.validate():
        location_name = form.autocomp.data
        return redirect(url_for('main.location', location=location_name))
    else:
        
        content = {
            'form': form
        }
        return render_template('/main/main.html', **content)
 


@main.route('/location', methods=['GET','POST'])
def location():
    form = SearchForm(request.form)

    content = {
        'form': form
    }
    return render_template('/main/location.html', **content)



@main.route('/directions', methods=['GET','POST'])
def directions():
    form = SearchForm(request.form)
    content = {
        'form': form
    }
    return render_template('/main/directions.html', **content)


@main.route('/route', methods=['GET','POST'])
@main.route('/route/<user>', methods=['GET','POST'])
@login_required
def route(user):
    form = RouteForm(request.form)

    content = {
        "form" : form
    }
    return render_template('/main/route.html', **content)

@main.route('/explore', methods=['GET'])
@login_required
def poi():
    form = SearchForm(request.form)
    poi_type_checkbox = PoiTypeForm(request.form)
    content = {
        'form': form,
        'poi_type_checkbox':poi_type_checkbox
    }
    return render_template('/main/explore.html', **content)

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
                new_user = User.add_user_to_db(email=form.email.data,password=form.password.data)
                login_user(new_user)

                return 'User created'
    else:
        'Form error'

@main.route('/login', methods=['GET','POST'])
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

@main.route('/user_dashboard/<user>', methods=['GET'])
@login_required
def user_dashboard(user):
    user = User.get_user(user)
    content = {
        "user": user
    }

    return render_template('/main/user_dashboard.html', **content)


@main.route('/_autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('query')
    payload = {
        'api_key' : mapzen_api,
        'text': query,
        'size' : 10,
        'layers': 'locality',
        'boundary.country': 'FRA'
        }
    
    mapzen_req = requests.get(url='https://search.mapzen.com/v1/search', params=payload)
    mapzen_resp_json = mapzen_req.json()

    json = { "query": "Unit","suggestions": [] }
    for result in mapzen_resp_json['features']:
        json["suggestions"] \
            .append({
                "value":','.join([result['properties']['name'],result['properties']['region']]),
                "data": result['geometry']['coordinates'] \
                })

    return jsonify(json)

@main.route('/_geocode', methods=['GET'])
def geocode():
    pass
