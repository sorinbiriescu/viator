import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True

SECRET_KEY = 'secretkey'

POSTGRES = {
    'user': 'postgres',
    'pw': 'admin',
    'db': 'VIATOR',
    'host': 'localhost',
    'port': '5432',
}

# RhoneAlpes = {
#     'user': 'postgres',
#     'pw': 'admin',
#     'db': 'RhoneAlpes',
#     'host': 'localhost',
#     'port': '5432',
# }
SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
# SQLALCHEMY_BINDS = {
#     'gis_rhone_alpes':'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % RhoneAlpes
# }

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db/db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False
JSON_AS_ASCII = False
SESSION_COOKIE_HTTPONLY = True
REMEMBER_COOKIE_HTTPONLY = True
