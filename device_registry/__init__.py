from flask import Flask
import os
from flask_restplus import Api

from flask_sqlalchemy import SQLAlchemy
from bestrouterec.document import db
from bestrouterec.api import api as recommendation_api


# Create an instance of Flask
app = Flask(__name__)

# Create the API
api = Api(app)

# def create_app(
#     api: Api = None,
#     redshift_db: SQLAlchemy = None,
# ) -> Flask:

#     app=Flask(__name__)

#     app.config[
#         "SQLALCHEMY_DATABASE_URI"
#     ] = 'postgres://admin:secret@localhost:5432/postgres'

#     app.config["SQLALCHEMY_ECHO"] = False
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#     redshift_db.init_app(app)
#     app.app_context().push()
#     with app.app_context():
#         redshift_db.create_all()

#     return app


class DeviceList:

    def get(self):
        return {'message': 'Success'}, 200


    def post(self):
        # parser = reqparse.RequestParser()

        # parser.add_argument('identifier', required=True)
        # parser.add_argument('name', required=True)
        # parser.add_argument('device_type', required=True)
        # parser.add_argument('controller_gateway', required=True)

        # # Parse the arguments into an object
        # args = parser.parse_args()

        # shelf = get_db()
        # shelf[args['identifier']] = args

        return {'message': 'Device registered'}, 201


class Device:
    def get(self, identifier):
        return {'message': 'Device found'}, 200

    def delete(self, identifier):
        return {'message': 'Device not found', 'data': {}}, 404



api.add_resource(DeviceList, '/devices')
api.add_resource(Device, '/device/<string:identifier>')
