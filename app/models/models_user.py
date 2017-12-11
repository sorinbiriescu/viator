from app import db
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import JSON

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
