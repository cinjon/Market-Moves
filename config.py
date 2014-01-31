import os
CSRF_ENABLED = True
SECRET_KEY = os.environ.get('COINBASE_SECRET_KEY')
basedir = os.path.abspath(os.path.dirname(__file__))
