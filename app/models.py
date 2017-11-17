from app import db

class Locations(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.Text)
    location_parent = db.Column(db.Text)

    

class Attractions(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    attraction_name = db.Column(db.Text)
    attraction_location = db.Column(db.Text)