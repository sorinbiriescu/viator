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

def test_hello_world(app_test):
    res = app_test.get("/")

    assert res.status_code == 200
