import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True

SECRET_KEY = '~tx86xc9x1ftOxb6xa2xdsfd11kLsfxd1xdsfscex7fx14yx9e'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'db/VIATOR.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False
