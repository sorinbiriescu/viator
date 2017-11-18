from flask import Blueprint, render_template, request
import folium
from app import Locations, Attractions
import os

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

    start_coords = (location_query.location_lat, location_query.location_long)
    map = folium.Map(location=start_coords, zoom_start=14)
    map.save(outfile=os.path.join(script_dir,"../templates/maps/map_%s.html" %(location_query.location_name)),
            close_file=True)

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