import sys

from flask import Flask

sys.path.insert(0, "")


def create_app(*, config_object) -> Flask:
    """Create a flask app instance."""

    flask_app = Flask("app")
    flask_app.config.from_object(config_object)

    with flask_app.app_context():
        from ml_api.controllers.core import app

        flask_app.register_blueprint(app)

    return flask_app
