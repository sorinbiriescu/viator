"""
Documentation:

* https://docs.pytest.org/en/latest/
* https://docs.pytest.org/en/latest/fixture.html
* http://flask.pocoo.org/docs/latest/testing/
"""

import pytest

from app import app, db
from app import Locations, Attractions

@pytest.fixture
def app_test():
    app.config.from_object('tests/config_test')
    db.create_all()
    db.session.commit()

    yield app.test_client()

    db.session.remove()
    db.drop_all()

def test_index(app_test):
    request = app_test.get("/")

    assert request.status_code == 200


def test_location(app_test):
    location = Locations(location_name='Grenoble', location_parent='Isere')
    db.session.add(location)
    db.session.commit()

    request = app_test.get("/location/Grenoble")
    request_404 = app_test.get("/location/Lyon")

    assert request.status_code == 200
    assert request_404.status_code == 404

def test_attraction(app_test):
    attraction = Attractions(attraction_name='Bastille', attraction_location='Grenoble')
    db.session.add(attraction)
    db.session.commit()

    request = app_test.get("/attraction/Bastille")
    request_404 = app_test.get("/attraction/Cafe_des_Jeux")

    assert request.status_code == 200
    assert request_404.status_code == 404

def test_route(app_test):
    request = app_test.get("/route")

    assert request.status_code == 200

@pytest.mark.xfail
def test_get_map(app_test):
    request = app_test.get("/get_route?location=Grenoble")

    assert request.status_code == 200