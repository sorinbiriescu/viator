import json

import geojson
from geoalchemy2 import Geography, Geometry, WKTElement
from geojson import Feature, FeatureCollection, Point
from jsonschema import validate
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
                        Locations.id,
                        Locations.name,
                        func.ST_AsGeoJSON(func.ST_FlipCoordinates(Locations.geometry))
                        ) \
                    .all()
        result_json = { "query": "Unit","suggestions": [] }
        
        for result in query:

            # This is required because the PostGIS function already creates
            # the GeoJSON and after it will be double encoded if used with
            # Flask jsonify. However jsonify is required to return the response
            # in json format.

            geo_json = json.loads(result[2])
            result_json["suggestions"].append({"value":result[1],"data":{"location_ID": result[0],"geo_json":result[2]}})

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
    def get_poi(json_request_param,radius=3000):

        poi_response_schema = json.loads(open('./app/schema/poi_multiple_schema.json').read())

        location_ID = json_request_param["location_ID"]
        query = json_request_param["query"]
        page = json_request_param["page"]
        per_page = json_request_param["per_page"]

        location_geometry = Locations.query \
                                .filter(Locations.id == location_ID) \
                                .with_entities(
                                    func.ST_AsText(Locations.geometry)
                                    ) \
                                .first()

        attraction_geometry = Attractions.query \
                                .with_entities(
                                    func.ST_asText(Attractions.centroid)
                                    ) \
                                .first()

        print(location_geometry)
        print(attraction_geometry)

        query = Attractions.query \
                    .filter(
                        and_(or_(
                                Attractions.attraction_type==i for i in query
                                ),
                            func.ST_Contains(
                                location_geometry,
                                Attractions.centroid
                                )
                        )) \
                    .with_entities(
                            Attractions.name,
                            Attractions.attraction_type,
                            func.ST_X(Attractions.centroid),
                            func.ST_Y(Attractions.centroid)
                            ) \
                    .paginate(page=page, per_page=per_page)

        print(query.items)

        result_json = {
            "total_results": query.total,
            "total_pages": query.pages,
            "current_page": query.page,
            # Note: PostGIS has coords in lat/lng, but GeoJSON encodes in lng/lat
            # When creating the point, it's required to reverse the coords.
            "result_geojson": FeatureCollection([Feature(geometry=Point((e[3],e[2])),properties={"name":e[0],"type":e[1]}) for e in query.items])
        }

        try:
            validate(result_json, poi_response_schema)
            print(result_json)
            return result_json
        except Exception as e:
            print("An error occured with the data format: ")
            print(str(e))
