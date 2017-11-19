import os

import folium
from flask import Blueprint, render_template, request

from app import Attractions, Locations

from ..maps.maps import create_map_att, create_map_loc

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
def location(location):

    location_query = Locations.get_location(location)
    create_map_loc(location_query)
    
    content = {
        'location' : location_query
    }

    return render_template('/main/location.html', **content)

@main.route('/attraction/<attraction>')
def attraction(attraction):

    attraction_query = Attractions.get_attraction(attraction)
    create_map_att(attraction_query)
    content = {
        'attraction' : attraction_query
    }
    return render_template('/main/attraction.html', **content)

@main.route('/route')
def route():
    return render_template('/main/route.html')
