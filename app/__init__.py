from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object('config')

from .models import Locations, Attractions

from .views.main import main
app.register_blueprint(main)
