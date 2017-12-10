from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin
from flask_login import LoginManager

app = Flask(__name__)

CORS(app)
app.config.from_object('config')

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "main.login"

@login_manager.user_loader
def load_user(email):
    return User.query.filter_by(email = email).first()


from .models.models import Locations, Attractions
from .models.models_user import User, UserRoute
from .models.gis_rhone_alpes import (
    rhone_alpes_line, rhone_alpes_nodes, rhone_alpes_point,
    rhone_alpes_polygon,rhone_alpes_rels,rhone_alpes_roads,rhone_alpes_ways) 
from .models.gis_methods import locationDefinition,get_poi_type
from .forms.forms_main import SearchForm, PoiTypeForm, LoginForm, SignupForm, Route
from .views.views_main import main
app.register_blueprint(main)
