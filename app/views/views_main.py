import os
import sys

import requests
from flask import (Blueprint, Response, jsonify, redirect, render_template,
                   request, url_for)

from app import (Attractions, Locations, SearchForm, SearchForm2, SearchForm3,
                 get_restaurants)

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

    return jsonify(json)

@main.route('/_getpoi', methods=['GET','POST'])
def getpoi():

    result = get_restaurants()

    return jsonify(result)

@main.route('/_geocode', methods=['GET'])
def geocode():
    pass

@main.route('/_optimized_route', methods=['GET','POST'])
def optimized_route():
    json = request.json
    payload = {
        "json" : json,
        "api_key" : mapzen_api,
        }
    print(json, file=sys.stderr)
    mapzen_req = requests.post(url='https://matrix.mapzen.com/optimized_route', params=payload)
    mapzen_resp_json = mapzen_req.json
    print(mapzen_req, file=sys.stderr)
    print(mapzen_req.json, file=sys.stderr)
    return mapzen_resp_json

# @main.after_request
# def after(response):
#   # todo with response
#     print(response.status)
#     print(response.headers)
#     print(response.get_data())
#     return response

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
    form2 = SearchForm2(request.form)
    content = {
        'form': form,
        'form2': form2
    }
    return render_template('/main/directions.html', **content)

@main.route('/route')
def route():
    form = SearchForm(request.form)
    form2 = SearchForm2(request.form)
    form3 = SearchForm3(request.form)
    content = {
        'form': form,
        'form2': form2,
        'form3': form3
    }
    return render_template('/main/route.html', **content)

@main.route('/poi', methods=['GET'])
def poi():
    form = SearchForm(request.form)
    content = {
        'form': form
    }
    return render_template('/main/poi.html', **content)
