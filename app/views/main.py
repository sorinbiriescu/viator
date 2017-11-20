import os

from flask import Blueprint, render_template, request, jsonify, Response
from wtforms import TextField, Form
import json

from app import Attractions, Locations

from ..maps.mapbox import get_geocode

script_dir = os.path.dirname(__file__)

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('/main/index.html')

cities = ["Bratislava",
          "Bratislava2",
          "Banská Bystrica",
          "Prešov",
          "Považská Bystrica",
          "Žilina",
          "Košice",
          "Ružomberok",
          "Zvolen",
          "Poprad"]

class SearchForm(Form):
    autocomp = TextField('Insert City', id='city_autocomplete')

@main.route('/_autocomplete', methods=['GET'])
def autocomplete():
    return Response(json.dumps(cities), mimetype='application/json')

@main.route('/location/<location>', methods=['GET', 'POST'])
def location(location):
    geocode = get_geocode(location)
    form = SearchForm(request.form)
    content = {
        'location_lat' : geocode[0],
        'location_long': geocode[1],
        'form': form
    }
    return render_template('/main/location.html', **content)

@main.route('/route')
def route():
    return render_template('/main/route.html')