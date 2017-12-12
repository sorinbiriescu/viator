import ast

from flask import jsonify
from geoalchemy2 import Geography, WKTElement
from sqlalchemy import and_, cast, func, or_
from sqlalchemy.sql import select

from app import (app, db, rhone_alpes_line, rhone_alpes_nodes, rhone_alpes_point,
                 rhone_alpes_polygon, rhone_alpes_rels, rhone_alpes_roads,
                 rhone_alpes_ways)


class locationDefinition(db.Model):

    __bind_key__ = None
    
    id = db.Column(db.Integer, primary_key=True)
    location_type = db.Column(db.Text)
    location_icon = db.Column(db.Text)
    location_color = db.Column(db.Text)
    location_shape = db.Column(db.Text)

    @staticmethod
    def fetch_definition(location_type):

        result = locationDefinition.query \
                        .filter(locationDefinition.location_type == location_type) \
                        .first()
        return result

def get_poi_type(json):

#   Query the database by type of amenity and gets as well the LatLong with
#   func ST_AsGeoJSON(column).
#   See http://www.postgis.org/docs/ST_AsGeoJSON.html for more
#
#   Query result should look like this:
#   [("L'Auberge Fleurie", 'restaurant', '{"type":"Point","coordinates":[4.3103263,45.7454795]}'),...]
#
#   Note that ST_GeoJSON returns in LongLat !!!

    location = WKTElement('POINT(%s %s)' % (json["coordinates"][1],json["coordinates"][0]), srid=4326)
    query = json["query"]
    page = json["page"]
    per_page=json["per_page"]

    query = rhone_alpes_point.query \
                .filter(and_(or_(
                                rhone_alpes_point.amenity==i for i in query
                                ),
                            func.ST_DWithin(cast(rhone_alpes_point.way,Geography),location, 3000)
                    )) \
                .with_entities(
                        rhone_alpes_point.osm_id,
                        rhone_alpes_point.name,
                        rhone_alpes_point.amenity,
                        func.ST_AsGeoJSON(rhone_alpes_point.way)
                        ) \
                .paginate(page=page, per_page=per_page)

    result = {
        "status":"OK",
        "total_results": query.total,
        "total_pages": query.pages,
        "current_page": query.page,
        "result":[{
                "oid":e[0],
                "osm_type":"point",
                "name":e[1],
                "type":e[2],
                "location":ast.literal_eval(e[3]),
                "icon":locationDefinition.fetch_definition(e[2]).location_icon,
                "color":locationDefinition.fetch_definition(e[2]).location_color,
                "shape":locationDefinition.fetch_definition(e[2]).location_shape} for e in query.items]
    }

    return result
