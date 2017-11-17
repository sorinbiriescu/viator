"""
Documentation:

* https://docs.pytest.org/en/latest/
* https://docs.pytest.org/en/latest/fixture.html
* http://flask.pocoo.org/docs/latest/testing/
"""
import os

import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app import app, db
from app.models import Locations, Attractions

@pytest.fixture
def app_test():
    """Session-wide test `Flask` application."""
    app.config.from_object('tests/config_test')
    db.init_app(app)
    with app.app_context():
        db.create_all()
        db.session.commit()
        
        yield app

        db.session.remove()
        db.drop_all()

def test_post_model(app_test):
    location = Locations(location_name='Grenoble',location_parent='Isere')
    attraction = Attractions(attraction_name='Bastille',attraction_location='Grenoble')

    db.session.add(location)
    db.session.add(attraction)
    db.session.commit()

    assert Locations.query.count() > 0
    assert Attractions.query.count() > 0

def test_location_queries(app_test):
    location = Locations(location_name='Grenoble',location_parent='Isere')
    
    db.session.add(location)
    db.session.commit()

    location_query_result = Locations.get_location('Grenoble')

    assert location_query_result.location_name == 'Grenoble'
    assert location_query_result.location_parent == 'Isere'

def test_attraction_queries(app_test):
    attraction = Attractions(attraction_name='Bastille',attraction_location='Grenoble')

    db.session.add(attraction)
    db.session.commit()

    attraction_query_result = Attractions.get_attraction('Bastille')

    assert attraction_query_result.attraction_name == 'Bastille'
    assert attraction_query_result.attraction_location == 'Grenoble'