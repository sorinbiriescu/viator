import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True

SECRET_KEY = '~t\x86\xc9\x1ew\x8bOcX4385O\xb6\xa2\x11kL\xd1\xce\x7f\x14<y\x9e'
TESTDB_PATH = os.path.join(basedir, 'db/VIATOR_test.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + TESTDB_PATH
SQLALCHEMY_TRACK_MODIFICATIONS = False
TESTING = True
