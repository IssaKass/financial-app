"""
Flask App Factory

This module provides a factory function `create_app` to create and configure a Flask app.
The app is configured based on the specified environment using the `get_config` function from
the `config` module. The following extensions are initialized:
- Flask-Migrate for database migrations
- Flask-CORS for enabling Cross-Origin Resource Sharing (CORS)
- Flask-JWT for JSON Web Token (JWT) support

The app registers several blueprints for organizing routes:
- auth_bp: Blueprint for authentication routes
- users_bp: Blueprint for user-related routes
- projects_bp: Blueprint for project-related routes
- subscriptions_bp: Blueprint for subscription-related routes
- export_bp: Blueprint for export-related routes

After configuration, the app context is updated with the current app's configuration.

Example Usage:
    app = create_app(environment="production")
"""

import os
from flask import Flask, current_app, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from config import get_config
from api.extensions import db, jwt
from api.routes import auth_bp, users_bp, projects_bp, subscriptions_bp


def create_app():
    """Create and configure the Flask app."""

    app = Flask(__name__)

    # Load configuration based on the specified environment
    flask_env = os.getenv("FLASK_ENV")
    app.config.from_object(get_config(flask_env))

    @app.route("/test")
    def test():
        return jsonify({"flask_env": flask_env, "test": "test"})

    # Initialize the database extension
    db.init_app(app)

    # Initialize the migration extension
    Migrate(app, db)

    # Enable CORS for all routes
    CORS(app)

    # Initialize the JWT extension
    jwt.init_app(app)

    # Register the blueprints with a specified prefix
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(subscriptions_bp)

    # Set the configuration in the current app context
    with app.app_context():
        current_app.config.update(app.config)

    return app
