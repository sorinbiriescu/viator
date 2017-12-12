import json

from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import JSON

from app import db


class User(UserMixin, db.Model):
    __bind_key__ = None

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40))
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    password_hash = db.Column(db.String)

    def __init__(self,email,password):
        self.email = email
        self.password = password

    def __repr__(self,):
        return '<User %r>' % self.email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.email)

    @staticmethod
    def get_user(email):
        query = User.query.filter(User.email == email).first()
        if query:
            return query
        else:
            return None
    
    @staticmethod
    def get_user_id(user):
        '''
        Returns the ID of the user. int format
        '''
        query = User.query.filter(User.email == user).first()
        if query:
            return int(query.id)
        else:
            return None

    @staticmethod
    def add_user_to_db(email,password):
        new_user = User(email=email,password=password)
        db.session.add(new_user)
        db.session.commit()

        return new_user

class UserRoute(db.Model):
    __bind_key__ = None

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    route_name = db.Column(db.String(80), nullable=False)
    route_JSON = db.Column(JSON)

    @staticmethod
    def get_user_routes(user):
        query = UserRoute.query.filter(UserRoute.user_id == user).all()

        if query:
            result = {"results":[{"route_id": e.id,"route_name":e.route_name} for e in query]}
            return result
        else:
            return None

    @staticmethod
    def add_route(user,route_name):
        new_route = UserRoute(user_id=user,route_name=route_name)
        db.session.add(new_route)
        db.session.commit()

    @staticmethod
    def delete_route(user_id, route_id, route_name):
        query = UserRoute.query \
                        .filter(
                            UserRoute.user_id == user_id,
                            UserRoute.id == route_id,
                            UserRoute.route_name == route_name
                            ) \
                        .first()
        db.session.delete(query)
        db.session.commit()

    @staticmethod
    def add_poi_to_route(user_id,route_id,poi_id):
        query = UserRoute.query \
                        .filter(
                            UserRoute.user_id == user_id,
                            UserRoute.id == route_id
                        ) \
                        .first()
        
        oid = poi_id.split(".")[0]
        oid_type = poi_id.split(".")[1]

        # if query.route_JSON is "":
        route = {
            "route_id" : 0,
            "old_route_id" : "",
            "oid" : oid,
            "oid_type" : oid_type
        }

        route_json = json.dumps(route)
        query.route_JSON = route_json
        db.session.commit()
