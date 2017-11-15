"""
Documentation

See also https://www.python-boilerplate.com/flask
"""
import os

from flask import Flask, render_template
from .views.main import main

app = Flask(__name__)
app.register_blueprint(main)
