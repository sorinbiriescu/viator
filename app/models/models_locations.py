import json

from geoalchemy2 import Geometry
from sqlalchemy import Column, and_, func

from app import db

from flask import jsonify


class Locations(db.Model):
    __bind_key__ = None

    id = db.Column(db.Integer, primary_key=True)
    osm_id = db.Column(db.Integer)
    name = db.Column(db.Text)
    decription = db.Column(db.Text)
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
        json_autocomplete = { "query": "Unit","suggestions": [] }
        
        print(json)
        for result in query:
            data = json.loads(result[1])
            json_autocomplete["suggestions"].append({"value":result[0],"data":data})

        return json_autocomplete

    
class Attractions(db.Model):

    __bind_key__ = None
    
    id = db.Column(db.Integer, primary_key=True)
    attraction_name = db.Column(db.Text)
    attraction_location = db.Column(db.Text)
    attraction_type = db.Column(db.Text)
    attraction_lat = db.Column(db.Float)
    attraction_long = db.Column(db.Float)

    @staticmethod
    def get_attraction(attraction):
        return Attractions.query \
                    .filter(Attractions.attraction_name == attraction) \
                    .first_or_404()
