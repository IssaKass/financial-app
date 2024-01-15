# """Main script to run the Flask application."""

from flask_cors import CORS
import os
from flask import Flask, jsonify
from flask_migrate import Migrate
from config import get_config
from api.extensions import db, jwt
from api.routes import auth_bp, users_bp, projects_bp, subscriptions_bp

app = Flask(__name__)

CORS(app)

# # Load configuration based on the specified environment
flask_env = os.getenv("FLASK_ENV")
app.config.from_object(get_config(flask_env))


@app.route("/")
def index():
    return jsonify(
        {
            "ENV": flask_env,
            "DEBUG": app.config["DEBUG"],
            "TESTING": app.config["TESTING"],
            "SECRET_KEY": app.config["SECRET_KEY"],
            "JWT_SECRET_KEY": app.config["JWT_SECRET_KEY"],
            "SQLALCHEMY_DATABASE_URI": app.config["SQLALCHEMY_DATABASE_URI"],
        }
    )


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


if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("PORT", default=5000))
