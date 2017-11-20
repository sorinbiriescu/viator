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

class SearchForm(Form):
    autocomp = TextField('Insert City', id='location-search-autocomplete')

@main.route('/_autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('query')
    result = Locations.get_location_autocomplete(query)
    return jsonify(result)

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