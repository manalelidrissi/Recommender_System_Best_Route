import datetime
import json

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Event(db.Model):


    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(), unique=False, nullable=False, index=True)
    trip_id = db.Column(db.String(), unique=False, nullable=False, index=True)
    timestamp = db.Column(db.DateTime, unique=False, nullable=False)


class Trips(db.Model):


    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trip_id = db.Column(db.String(), unique=False, nullable=False, index=True)
    distance = db.Column(db.String(), unique=False, nullable=False)
    departure_point = db.Column(db.String(), unique=False, nullable=False)
    arrival_point = db.Column(db.String(), unique=False, nullable=False)
    departure_timestamp = db.Column(db.DateTime, unique=False, nullable=False)
    arrival_timestamp = db.Column(db.DateTime, unique=False, nullable=False)