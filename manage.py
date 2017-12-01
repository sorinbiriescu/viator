from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, prompt_bool

from app import app, db

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def initdb():
    db.create_all(bind=None) #bind=None if only the main DB needs to be created
    db.session.commit()
    print('Initialized the database')


@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all(bind=None)
        print('Dropped the database')


if __name__ == '__main__':
    manager.run()
