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
    app.debug = True
    app.testing = True
    return app.test_client()


def test_hello_world(app_test):
    res = app_test.get("/")
    # print(dir(res), res.status_code)
    assert res.status_code == 200
