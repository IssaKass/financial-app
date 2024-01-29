# """Main script to run the Flask application."""

import os
from flask_cors import CORS
from flask import Flask
from flask_migrate import Migrate
from config import get_config
from api.extensions import db, jwt
from api.routes import (
    auth_bp,
    users_bp,
    projects_bp,
    subscriptions_bp,
    tasks_bp,
    export_bp,
)

app = Flask(__name__)

CORS(app)

# # Load configuration based on the specified environment
flask_env = os.getenv("FLASK_ENV")
app.config.from_object(get_config(flask_env))

# Initialize the database extension
db.init_app(app)

# Initialize the migration extension
Migrate(app, db)

# Initialize the JWT extension
jwt.init_app(app)

# Register the blueprints with a specified prefix
app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)
app.register_blueprint(projects_bp)
app.register_blueprint(subscriptions_bp)
app.register_blueprint(tasks_bp)
app.register_blueprint(export_bp)


if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("PORT", default=5000))
