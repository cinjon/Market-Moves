from flask.ext.script import Manager
from app import flask_app
import cron

manager = Manager(flask_app)

@manager.command
def update_records():
    cron.update_records()

if __name__ == '__main__':
    manager.run()
