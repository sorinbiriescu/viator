from flask import Blueprint, render_template, request
import folium
from app import Locations, Attractions
import os
from ..maps.maps import create_map

script_dir = os.path.dirname(__file__)

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('/main/index.html')

@main.route('/get_map')
def get_map():
    location = request.args.get('location')
    return render_template('/maps/map_%s.html' % (location))

@main.route('/location/<location>')
def location(location='Grenoble'):

    location_query = Locations.get_location(location)
    create_map(location_query)
    
    content = {
        'location' : location_query
    }

    return render_template('/main/location.html', **content)

@main.route('/attraction/<attraction>')
def attraction(attraction):

    attraction_query_result = Attractions.get_attraction(attraction)
    content = {
        'attraction' : attraction_query_result
    }
    return render_template('/main/attraction.html', **content)

@main.route('/route')
def route():
    return render_template('/main/route.html')