from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
app.config.from_object('config')
db = SQLAlchemy(app)

from .models.models import Locations, Attractions
from .models.gis_rhone_alpes import (
    rhones_alpes_line, rhones_alpes_nodes, rhones_alpes_point,
    rhones_alpes_polygon,rhones_alpes_rels,rhones_alpes_roads,rhones_alpes_ways) 
from .forms.forms_main import SearchForm, SearchForm2, SearchForm3
from .views.views_main import main
app.register_blueprint(main)