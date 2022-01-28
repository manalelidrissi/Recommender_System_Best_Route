import datetime
import json

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

def create_app(
    redshift_db: SQLAlchemy,
) -> Flask:

    app=Flask(__name__)

    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = 'postgres://admin:secret@localhost:5432/postgres'

    app.config["SQLALCHEMY_ECHO"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    redshift_db.init_app(app)
    app.app_context().push()
    with app.app_context():
        redshift_db.create_all()

    #api.init_app(app)

    return app


db = SQLAlchemy(create_app(db))


class Event(db.Model):


    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(), unique=False, nullable=False, index=True)
    trip_id = db.Column(db.String(), unique=False, nullable=False, index=True)
    timestamp = db.Column(db.DateTime, unique=False, nullable=False)

class Trip(db.Model):


    trip_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    distance = db.Column(db.String(), unique=False, nullable=False)
    departure_point = db.Column(db.String(), unique=False, nullable=False)
    arrival_point = db.Column(db.String(), unique=False, nullable=False)
    departure_timestamp = db.Column(db.DateTime, unique=False, nullable=False)
    arrival_timestamp = db.Column(db.DateTime, unique=False, nullable=False)
    transport = db.Column(db.String(), unique=False, nullable=False)