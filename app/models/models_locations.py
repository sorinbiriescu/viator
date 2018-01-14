import ast
import json

import shapely.wkt
from flask import jsonify
from geoalchemy2 import Geography, Geometry, WKTElement
from geojson import Feature, FeatureCollection
from sqlalchemy import Column, and_, cast, func, or_

from app import db


class Locations(db.Model):
    __bind_key__ = None

    id = db.Column(db.Integer, primary_key=True)
    osm_id = db.Column(db.Integer)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    admin_type = db.Column(db.Text)
    admin_level = db.Column(db.Integer)
    centroid = db.Column(Geometry('POINT'))
    geometry = db.Column(Geometry('GEOMETRY'))

    @staticmethod
    def get_location_autocomplete(term):
        query =  Locations.query \
                    .filter(Locations.name.like(term+'%')) \
                    .with_entities(
                        Locations.name,
                        func.ST_AsGeoJSON(Locations.geometry)) \
                    .all()
        result_json = { "query": "Unit","suggestions": [] }
        
        print(json)
        for result in query:

            # This is required because the PostGIS function already creates
            # the GeoJSON and after it will be double encoded if used with
            # Flask jsonify. However jsonify is required to return the response
            # in json format.

            data = json.loads(result[1])
            result_json["suggestions"].append({"value":result[0],"data":data})

        return result_json

class Attractions(db.Model):

    __bind_key__ = None
    
    id = db.Column(db.Integer, primary_key=True)
    osm_id = db.Column(db.BigInteger)
    osm_type = db.Column(db.Text)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    attraction_type = db.Column(db.Text)
    centroid = db.Column(Geometry('POINT'))

    @staticmethod
    def get_poi_by_distance(json_request_param,radius=3000):

        location = WKTElement('POINT(%s %s)' % (json_request_param["coordinates"]["lat"],json_request_param["coordinates"]["lng"]), srid=4326)
        query = json_request_param["query"]
        page = json_request_param["page"]
        per_page = json_request_param["per_page"]

        query = Attractions.query \
                    .filter(and_(or_(
                                    Attractions.attraction_type==i for i in query
                                    ),
                                func.ST_DWithin(cast(Attractions.centroid,Geography),location, radius)
                        )) \
                    .with_entities(
                            Attractions.name,
                            Attractions.attraction_type,
                            func.ST_AsText(Attractions.centroid)
                            ) \
                    .paginate(page=page, per_page=per_page)

        
        result_json = {
            "total_results": query.total,
            "total_pages": query.pages,
            "current_page": query.page,
            "result_geojson": FeatureCollection([Feature(geometry=shapely.wkt.loads(e[2]),properties={"name":e[0],"type":e[1]}) for e in query.items])
                
        }

        return result_json
