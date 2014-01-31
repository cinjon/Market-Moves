import os
CSRF_ENABLED = True
SECRET_KEY = os.environ.get('MARKETMOVES_SECRET_KEY')
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', os.environ.get('MARKETMOVER_DATABASE_URL'))
