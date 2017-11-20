from app import db

class Locations(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    location_eu_region = db.Column(db.Text)
    location_region_code = db.Column(db.Integer)
    location_region_name = db.Column(db.Text)
    location_region_capital = db.Column(db.Text)
    location_department_no = db.Column(db.Integer)
    location_department_name = db.Column(db.Text)
    location_prefecture = db.Column(db.Text)
    location_circumscription = db.Column(db.Integer)
    location_name = db.Column(db.Text)
    location_postal_code = db.Column(db.Integer)
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
                    .with_entities(Locations.location_name,Locations.location_department_name) \
                    .filter(Locations.location_name.like(term+'%')) \
                    .all()
        json = { "query": "Unit","suggestions": [] }
        for result in query:
            json["suggestions"].append({"value":','.join([result[0],result[1]]),"data":','.join([result[0],result[1]])})
        return json

class Attractions(db.Model):

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
