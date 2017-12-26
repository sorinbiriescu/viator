import json
import os
import sys

import requests
from flask import Blueprint, jsonify, request
from flask_login import current_user

from app.models.gis_methods import get_poi_type
from app.models.models_user import User, UserRoute

mapzen_api = 'mapzen-fPCfu1G'

script_dir = os.path.dirname(__file__)

api = Blueprint('api', __name__, url_prefix='/api')

mapzen_api = 'mapzen-fPCfu1G'

@api.route('/autocomplete', methods=['GET'])
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

@api.route('/route', methods=['GET','POST','PUT','DELETE'])
def route_api():
    '''
    Create / delete user routes
    '''
    user = User.get_user_id(current_user.email)

    if request.method == 'GET':
        routes = UserRoute.get_user_routes(user)

        return jsonify(routes)

    elif request.method == 'POST':
        route_json = request.json
        UserRoute.add_route(user = user, route_name = route_json["route_name"])

        return jsonify({"status":"200"})

    elif request.method == 'DELETE':
        route_json = request.json
        UserRoute.delete_route(user_id=user,route_id=route_json["route_id"],route_name=route_json["route_name"])
        
        return jsonify({"status":"200"})

@api.route('/route_poi', methods=['GET','POST','PUT','DELETE'])
def route_poi_api():
    '''
    Add, remove, delete or change the position of a POI in a route
    '''
    user = User.get_user_id(current_user.email)

    if request.method == 'GET':
        route_id = request.args.get("route_id")
        result = UserRoute.get_poi_route(user, route_id)
        return jsonify(result)

    elif request.method == 'POST':
        route = request.json
        UserRoute.add_poi_to_route(user,route["route_id"],route["poi_id"])
        return "OK"

    elif request.method == 'PUT':
        param = request.json
        UserRoute.change_poi_pos_in_route(
            route_id= param["route_id"],
            poi_pos= param["poi_pos"],
            poi_new_pos= param["poi_new_pos"],
            user_id = user )
        return "OK"

    elif request.method == 'DELETE':
        request_json = request.json
        route_id = request_json["route_id"]
        poi_pos = request_json["poi_pos"]
        UserRoute.remove_poi_from_route(route_id = route_id, poi_pos = poi_pos, user_id = user)

        return "OK"



@api.route('/optimized_route', methods=['GET','POST'])
def optimized_route_api():
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


@api.route('/getpoi', methods=['GET','POST'])
def getpoi():
    '''
    Get POI around 3km of a given point
    '''
    json_response = request.json
    result = get_poi_type(json_response)

    return json.dumps(result)


@api.route('/turnbyturn', methods =['GET'])
def turnbyturn():
    '''
    Calls mapzen to get a route between given POIs in a route
    '''

