from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, prompt_bool

from app import app, db

import app.models

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def initdb():
    db.create_all()
    db.session.commit()
    print('Initialized the database')


@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()
        print('Dropped the database')


if __name__ == '__main__':
    manager.run()
