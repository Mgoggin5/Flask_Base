from flask import Flask, request
from mongokit import Connection, Document
from config.base import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask.ext.mongokit import MongoKit, Document

from redis import Redis, RedisError


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
Document = Document
Connection = Connection(app.config['MONGODB_HOST'], app.config['MONGODB_PORT'])
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)
moment = Moment(app)
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)


from app import routes, models 