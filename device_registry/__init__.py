import os
import shelve

# Import the framework
from flask import Flask, g
from flask_restful import Resource, Api, reqparse

# Create an instance of Flask
app = Flask(__name__)

# Create the API
api = Api(app)


class DeviceList(Resource):
    def get(self):

        return {'message': 'Success'}, 200

    def post(self):

        return {'message': 'Device registered'}, 201


class Device(Resource):
    def get(self, identifier):

        return {'message': 'Device found'}, 200

    def delete(self, identifier):

        return {'message': 'Device not found', 'data': {}}, 404



api.add_resource(DeviceList, '/devices')
api.add_resource(Device, '/device/<string:identifier>')




