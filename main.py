"""Main script to run the Flask application."""

from api import create_app
from api.extensions import db

if __name__ == "__main__":
    environment = "development"

    APP = create_app(environment)

    if environment == "testing":
        with APP.app_context():
            db.drop_all()
            db.create_all()

    APP.run(debug=True, port=5000)
