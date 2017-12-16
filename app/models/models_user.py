import json

from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import JSON

from app import db
from app.models.gis_methods import get_poi_by_oid


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
    def get_poi_route(user_id,route_id):
        query = UserRoute.query \
                        .filter(
                            UserRoute.user_id == user_id,
                            UserRoute.id == route_id
                        ) \
                        .first()

        route_json = json.loads(query.route_JSON)

        for i in route_json["route"]:
            oid = i["oid"]
            oid_query = get_poi_by_oid(oid)
            print(oid_query)
            i.update(
                {
                    "name": oid_query[1],
                    "type": oid_query[2],
                    "coordinates": oid_query[3]
                }
        )
        
        return route_json

    @staticmethod
    def add_poi_to_route(user_id,route_id,poi_id):
        query = UserRoute.query \
                        .filter(
                            UserRoute.user_id == user_id,
                            UserRoute.id == route_id
                        ) \
                        .first()
        
        oid = int(poi_id.split(".")[0])
        oid_type = poi_id.split(".")[1]

        if query.route_JSON is None:
            route = {"route": [
                {
                "poi_pos" : 0,
                "old_poi_pos" : "",
                "oid" : oid,
                "oid_type" : oid_type
                }
            ]}

            route_json = json.dumps(route)
            query.route_JSON = route_json
            db.session.commit()
        else:
            route_json = json.loads(query.route_JSON)
            last_route_id = max(route_json["route"], key=lambda x:x["poi_pos"])["poi_pos"]
            route_json["route"].append(
                {
                "poi_pos" : (last_route_id+1),
                "old_poi_pos" : "",
                "oid" : oid,
                "oid_type" : oid_type
                }
            )
            query.route_JSON = json.dumps(route_json)
            db.session.commit()

    @staticmethod
    def remove_poi_from_route(route_id,poi_pos, user_id):
        query = UserRoute.query \
                .filter(
                    UserRoute.user_id == user_id,
                    UserRoute.id == route_id
                ) \
                .first()

        route_json = json.loads(query.route_JSON)

        for i in route_json["route"]:
            if i["poi_pos"] == int(poi_pos):
                route_json["route"].remove(i)
                break

        for i in route_json["route"]:
            if i["poi_pos"] > int(poi_pos):
                i["poi_pos"] -=1

        query.route_JSON = json.dumps(route_json)
        db.session.commit() 
        
        return "OK"
