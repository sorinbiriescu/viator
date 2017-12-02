from sqlalchemy import func
from sqlalchemy.sql import select

from app import (db, rhone_alpes_line, rhone_alpes_nodes, rhone_alpes_point,
                 rhone_alpes_polygon, rhone_alpes_rels, rhone_alpes_roads,
                 rhone_alpes_ways)

from flask import jsonify
import ast

def get_restaurants():

#   Query the database by type of amenity and gets as well the LatLong with
#   func ST_AsGeoJSON(column).
#   See http://www.postgis.org/docs/ST_AsGeoJSON.html for more
#
#   Query result should look like this:
#   [("L'Auberge Fleurie", 'restaurant', '{"type":"Point","coordinates":[4.3103263,45.7454795]}'),...]
#
#   Note that ST_GeoJSON returns in LongLat !!!

    query = rhone_alpes_point.query \
                .filter(rhone_alpes_point.amenity=="restaurant") \
                .with_entities(
                        rhone_alpes_point.name,
                        rhone_alpes_point.amenity,
                        func.ST_AsGeoJSON(rhone_alpes_point.way)
                        ) \
                .limit(10) \
                .all()
    result = {
        "status":"OK",
        "result":[{"name":e[0], "type":e[1], "location":ast.literal_eval(e[2])} for e in query]}

    return result

