import os

from flask import Blueprint, render_template, request

from app import Attractions, Locations

from ..maps.mapbox import get_geocode

script_dir = os.path.dirname(__file__)

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('/main/index.html')

@main.route('/location/<location>')
def location(location):

    geocode = get_geocode(location)

    content = {
        'location_lat' : geocode[0],
        'location_long': geocode[1]
    }
    return render_template('/main/mapbox.html', **content)

@main.route('/route')
def route():
    return render_template('/main/route.html')