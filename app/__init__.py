from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .views.main import main

app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(main)

db = SQLAlchemy(app)
