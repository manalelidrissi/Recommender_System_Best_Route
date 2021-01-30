"""
This module is used for configuration of Flask application.
"""
import os


class Config:
    APP_PORT = int(os.environ.get("APP_PORT", default=5004))
