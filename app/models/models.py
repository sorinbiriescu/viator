from app import db
from sqlalchemy import Column,and_
import json

class Locations(db.Model):
    __bind_key__ = None

    id = db.Column(db.Integer, primary_key=True)
    location_eu_region = db.Column(db.Text)
    location_region_code = db.Column(db.Integer)
    location_region_name = db.Column(db.Text)
    location_region_capital = db.Column(db.Text)
    location_department_no = db.Column(db.Text)
    location_department_name = db.Column(db.Text)
    location_prefecture = db.Column(db.Text)
    location_circumscription = db.Column(db.Integer)
    location_name = db.Column(db.Text)
    location_postal_code = db.Column(db.Text)
    location_insee_code = db.Column(db.Integer)
    location_lat = db.Column(db.Float)
    location_long = db.Column(db.Float)
    location_distance = db.Column(db.Float)

    @staticmethod
    def get_location_unique(location):
        return Locations.query \
                    .filter(Locations.location_name == location) \
                    .first_or_404()

    @staticmethod
    def get_location_autocomplete(term):
        query =  Locations.query \
                    .with_entities(Locations.location_name,Locations.location_region_name) \
                    .filter(Locations.location_name.like(term+'%')) \
                    .all()
        json = { "query": "Unit","suggestions": [] }
        for result in query:
            json["suggestions"].append({"value":','.join([result[0],result[1],'France']),"data":','.join([result[0],result[1],'France'])})
        return json

    @staticmethod
    def get_geocode_local(term):
        term.replace("%2C", ",")
        search_term = term.split(",")
        if len(search_term) == 2:
            region_name = search_term[0]
        else:
            location_name = search_term[0]
            region_name = search_term[1]
        query = Locations.query \
                    .with_entities(Locations.location_name,
                        Locations.location_region_name,
                        Locations.location_lat,
                        Locations.location_long 
                        ) \
                    .filter(and_(Locations.location_name == location_name,
                            Locations.location_region_name == region_name) \
                        ) \
                    .first()
        if query.location_lat or query.location_long != 0.0:

            geocode = {'location_name': query.location_name,
                        'location_lat': query.location_lat,
                        'location_long': query.location_long }
            return json.dumps(geocode)

        else:
            return None

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
