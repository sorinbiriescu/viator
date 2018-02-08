import json
import os
import sys

import requests
from flask import Blueprint, jsonify, request
from flask_login import current_user

from app.models.models_user import User, UserRoute
from app.models.models_locations import Locations, Attractions

script_dir = os.path.dirname(__file__)

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('query')
    result = Locations.get_location_autocomplete(query)

    return jsonify(result)

@api.route('/itinerary', methods=['GET','POST','DELETE'])
def route_api():
    '''
    Create / delete user itineraries
    '''
    user = User.get_user_id(current_user.email)

    if request.method == 'GET':
        routes = UserRoute.get_user_routes(user)

        return jsonify(routes)

    elif request.method == 'POST':
        itinerary_json = request.json
        UserRoute.add_route(user = user, route_name = _json["route_name"])

        return jsonify({"status":"200"})

    elif request.method == 'DELETE':
        route_json = request.json
        UserRoute.delete_route(user_id=user,route_id=route_json["route_id"],route_name=route_json["route_name"])
        
        return jsonify({"status":"200"})

# @api.route('/route_poi', methods=['GET','POST','PUT','DELETE'])
# def route_poi_api():
#     '''
#     Add, remove, delete or change the position of a POI in a route
#     '''
#     user = User.get_user_id(current_user.email)

#     if request.method == 'GET':
#         route_id = request.args.get("route_id")
#         result = UserRoute.get_poi_route(user, route_id)
#         return jsonify(result)

#     elif request.method == 'POST':
#         route = request.json
#         UserRoute.add_poi_to_route(user,route["route_id"],route["poi_id"])
#         return "OK"

#     elif request.method == 'PUT':
#         param = request.json
#         UserRoute.change_poi_pos_in_route(
#             route_id= param["route_id"],
#             poi_pos= param["poi_pos"],
#             poi_new_pos= param["poi_new_pos"],
#             user_id = user )
#         return "OK"

#     elif request.method == 'DELETE':
#         request_json = request.json
#         route_id = request_json["route_id"]
#         poi_pos = request_json["poi_pos"]
#         UserRoute.remove_poi_from_route(route_id = route_id, poi_pos = poi_pos, user_id = user)

#         return "OK"

@api.route('/getpoi', methods=['GET'])
def getpoi():

    json_request_param = json.loads(request.args.get('parameters'))
    result = Attractions.get_poi(json_request_param)

    return jsonify(result)

