from app import db

class Locations(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.Text)
    location_parent = db.Column(db.Text)
    location_type = db.Column(db.Text)
    location_lat = db.Column(db.Float)
    location_long = db.Column(db.Float)

    @staticmethod
    def get_location(location):
        return Locations.query \
                    .filter(Locations.location_name == location) \
                    .first_or_404()

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
