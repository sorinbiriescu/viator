import os

from flask import Blueprint, Response, jsonify, render_template, request, url_for, redirect

from app import Attractions, Locations, SearchForm

from ..maps.mapbox import get_geocode

script_dir = os.path.dirname(__file__)

main = Blueprint('main', __name__)


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
    


@main.route('/_autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('query')
    result = Locations.get_location_autocomplete(query)
    return jsonify(result)

@main.route('/location/', methods=['GET','POST'])
def location():
    form = SearchForm(request.form)
    content = {
        # 'location_name': geocode[0]['location_name'],
        # 'location_lat' : geocode[0]['location_lat'],
        # 'location_long': geocode[0]['location_long'],
        'form': form
    }
    return render_template('/main/location.html', **content)

@main.route('/route')
def route():
    return render_template('/main/route.html')
