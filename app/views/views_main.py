import os
import requests

from flask import Blueprint, Response, jsonify, render_template, request, url_for, redirect

from app import Attractions, Locations, SearchForm

from ..maps.mapbox import get_geocode

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

    print(mapzen_req)

    return jsonify(json)


@main.route('/_geocode', methods=['GET'])
def geocode():
    query = request.args.get('query')
    local_db_query = Locations.get_geocode_local(query)
    if local_db_query is None:
        geocode = get_geocode(query)
        return geocode
    else:
        return local_db_query

@main.route('/location', methods=['GET','POST'])
def location():
    form = SearchForm(request.form)
    content = {
        # 'location_name': geocode[0]['location_name'],
        # 'location_lat' : geocode[0]['location_lat'],
        # 'location_long': geocode[0]['location_long'],
        'form': form
    }
    return render_template('/main/location.html', **content)

@main.route('/mapzen', methods=['GET','POST'])
def mapzen():
    form = SearchForm(request.form)
    content = {
        # 'location_name': geocode[0]['location_name'],
        # 'location_lat' : geocode[0]['location_lat'],
        # 'location_long': geocode[0]['location_long'],
        'form': form
    }
    return render_template('/main/mapzen.html', **content)

@main.route('/route')
def route():
    return render_template('/main/route.html')
