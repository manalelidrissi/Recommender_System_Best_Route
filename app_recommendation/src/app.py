import os
from flask_restplus import Api

from bestrouterec.document import db
from bestrouterec import api as recommendation_api

api = Api(title="ACM Recommendation")
api.add_namespace(recommendation_api)


APP_PORT = int(os.environ.get("APP_PORT", default=5000))

redshift_config = {
    "db": os.environ.get("REDSHIFT_DB_NAME", default="brr"),
    "host": os.environ.get("REDSHIFT_HOSTNAME", default="localhost"),
    "port": int(os.environ.get("REDSHIFT_PORT", default="5432")),
    "driver": os.environ.get("REDSHIFT_DRIVER", default="postgresql"),
    "username": os.environ.get("REDSHIFT_USERNAME", default="admin"),
    "password": os.environ.get("REDSHIFT_PASSWORD", default="admin"),
}

def create_app(
    api: Api,
    redshift_db: SQLAlchemy = None,
) -> Flask:
    """
    Application Factory for Flask App.

    :param api: the RestPlus api
    :param config: package path to config object.
    :param injector_modules:
    :param custom_injector:
    :param mongo_db: the MongoDB client.
    :param redshift_db: the SQLAlchemy client for Redshift.
    :return: configured flask app
    """
    app: Flask = Flask(__name__)

    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"{redshift_config['driver']}://{redshift_config['username']}:{redshift_config['password']}@{redshift_config['host']}:{redshift_config['port']}/{redshift_config['db']}"
    app.config["SQLALCHEMY_ECHO"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    redshift_db.init_app(app)
    with app.app_context():
        redshift_db.create_all()

    api.init_app(app)

    return app

app = create_app(
    api=api, redshift_db=db,
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app["APP_PORT"])
