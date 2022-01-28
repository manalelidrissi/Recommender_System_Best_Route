from flask import Flask
import os
from flask_restplus import Api

from flask_sqlalchemy import SQLAlchemy
from bestrouterec.document import db
from bestrouterec.api import api as recommendation_api

api = Api(title="ACM Recommendation")
api.add_namespace(recommendation_api)


def create_app(
    api: Api = None,
    redshift_db: SQLAlchemy = None,
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

#APP_PORT = int(os.environ.get("APP_PORT", default=5000))

appli = create_app(
    api=api, redshift_db=db,
)


if __name__ == "__main__":
   appli.run(host='127.0.0.1',port=4000,debug=True)
