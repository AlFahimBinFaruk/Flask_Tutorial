from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime

"""
This is an exaple of one to many relationships.
"""

class Note(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    data = db.Column(db.String(1500))
    date = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))

# for handlding user login we are going to use flask login so we also have to use UserMixin while difining user model
class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150),unique=True)
    password = db.Column(db.String(150))
    notes = db.relationship("Note")
