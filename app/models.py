from app import db

class Locations(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    company = db.Column(db.Text)
