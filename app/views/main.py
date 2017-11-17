from flask import Blueprint, render_template
from app.models import Locations, Attractions

main = Blueprint('main', __name__)



@main.route('/')
def index():
    return render_template('/main/index.html')



@main.route('/<location>')
def location(location):

    location_query_result = Locations.get_location(location)
    content = {
        'location' : location_query_result
    }
    return render_template('/main/location.html', **content)



@main.route('/<attraction>')
def attraction():

    attraction_query_result = Attractions.get_attraction(attraction)
    content = {
        'attraction' : attraction_query_result
    }
    return render_template('/main/attraction.html', **content)



@main.route('/route')
def route():
    return render_template('/main/route.html')