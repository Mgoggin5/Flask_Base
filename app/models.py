from datetime import datetime
from app import db

class User(db.Model):


    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):


    def __repr__(self):
        return '<Post {}>'.format(self.body)