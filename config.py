import os

from bookr.app import app

DEBUG = True
SECRET_KEY = 'dev'
DATABASE = os.path.join(app.root_path, 'main.db')
