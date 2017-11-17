"""
Documentation:

* https://docs.pytest.org/en/latest/
* https://docs.pytest.org/en/latest/fixture.html
* http://flask.pocoo.org/docs/latest/testing/
"""

import pytest

from app import app


@pytest.fixture
def app_test():
    app.config.from_object('tests/config_test')
    return app.test_client()

def test_index(app_test):
    request = app_test.get("/")

    assert request.status_code == 200

def test_location(app_test):
    request = app_test.get("/location")

    assert request.status_code == 200

def test_attraction(app_test):
    request = app_test.get("/attraction")

    assert request.status_code == 200

def test_route(app_test):
    request = app_test.get("/route")

    assert request.status_code == 200