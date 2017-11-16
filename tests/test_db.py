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
from app.models import Locations

app.config.from_object('tests/config_test')

@pytest.fixture
def app_init():
    """Session-wide test `Flask` application."""
    db.init_app(app)
    with app.app_context():
        db.create_all()
        db.session.commit()
        
        yield app

        # db.session.remove()
        # db.drop_all()

def test_post_model(app_init):
    post = Locations(location_name='foo',location_parent='bar')

    db.session.add(post)
    db.session.commit()

    assert post.id > 0
