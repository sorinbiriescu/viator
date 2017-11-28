from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
app.config.from_object('config')
db = SQLAlchemy(app)

from .models import Locations, Attractions
from .forms.forms_main import SearchForm, SearchForm2, SearchForm3
from .views.views_main import main
app.register_blueprint(main)