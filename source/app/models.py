from app import db, login, app
from app import mdb
from hashlib import md5
from datetime import datetime
from time import time
import jwt


from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))



class RedFish(mdb.EmbeddedDocument):

    restart = mdb.BooleanField(required = True)
    update = mdb.StringField(max_length = 255)

class BMC(mdb.EmbeddedDocument): 

    hostname = mdb.StringField(required = True)
    ip_address = mdb.StringField(required = True)
    redfish =  mdb.EmbeddedDocumentField(RedFish)


class Host(mdb.Document):

    hostname = mdb.StringField(required = True)
    os = mdb.StringField(max_length = 255)
    application = mdb.StringField(max_length = 255)
    bmc = mdb.EmbeddedDocumentField(BMC)