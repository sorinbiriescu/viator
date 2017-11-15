"""
Documentation

See also https://www.python-boilerplate.com/flask
"""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from .views.main import main

app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(main)

db = SQLAlchemy(app)
