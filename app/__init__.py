from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin
from flask_login import LoginManager

app = Flask(__name__)

CORS(app)
app.config.from_object('config')

db = SQLAlchemy(app)

from app.models.models_user import User, UserRoute
from app.models.models_locations import Locations, Attractions

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "main.login"
login_manager.session_protection = "strong"

@login_manager.user_loader
def load_user(email):
    return User.query.filter_by(email = email).first()


from .views.views_main import main
from .views.views_api import api

app.register_blueprint(main)
app.register_blueprint(api)
