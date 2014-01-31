from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

flask_app = Flask(__name__)
flask_app.config.from_object('config')
flask_app.debug = True
db = SQLAlchemy(flask_app)

import views
import models

@flask_app.before_first_request
def before_first_request():
    try:
        db.create_all()
    except Exception, e:
        flask_app.logger.error(str(e))
