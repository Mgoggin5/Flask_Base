import os
basedir = os.path.abspath(os.path.dirname(__file__))
from datetime import datetime


class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgres' or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MONGODB_DB = 'project1'
    MONGODB_HOST = 'mongodb'
    MONGODB_PORT = 27017
    