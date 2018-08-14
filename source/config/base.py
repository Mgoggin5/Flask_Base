import os
basedir = os.path.abspath(os.path.dirname(__file__))
from datetime import datetime


class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgres' or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MONGODB_HOST = os.environ.get('MONGODB_HOST') or 'mongodb'
    MONGO_PORT = os.environ.get('MONGODB_PORT') or 27017