"""User routes for the Flask application."""

from flask import Blueprint, request, jsonify
from api.models import User
from api.utils.regex import USERNAME_PATTERN, EMAIL_PATTERN, PASSWORD_PATTERN, validate
from api.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity

users_bp = Blueprint("users", __name__)


@users_bp.route("/users", methods=["GET"])
def get_all_users():
    """Get all users."""

    users = User.query.all()
    serialized_users = [user.serialize() for user in users]
    return jsonify(serialized_users), 200


@users_bp.route("/users", methods=["POST"])
def create_user():
    """Create a new user."""

    data = request.json

    required_fields = ["username", "email", "password"]

    if not all(field in data for field in required_fields):
        return jsonify({"message": "Username, email, and password are required"}), 400

    username = data["username"].strip()
    email = data["email"].strip()
    password = data["password"].strip()

    if not validate(username, USERNAME_PATTERN):
        return jsonify({"error": {"username": USERNAME_PATTERN["message"]}}), 400

    if not validate(email, EMAIL_PATTERN):
        return jsonify({"error": {"email": EMAIL_PATTERN["message"]}}), 400

    if not validate(password, PASSWORD_PATTERN):
        return jsonify({"error": {"password": PASSWORD_PATTERN["message"]}}), 400

    try:
        # Check if the username already exists
        existing_username = User.query.filter_by(username=username).first()

        if existing_username:
            return jsonify({"error": {"username": "Username already in use"}}), 400

        # Check if the email already exists
        existing_email = User.query.filter_by(email=email).first()

        if existing_email:
            return jsonify({"error": {"email": "Email already in use"}}), 400

        user = User(username=username, email=email, password=password)

        db.session.add(user)
        db.session.commit()

        return jsonify(user.serialize()), 201

    except ValueError as ve:
        db.session.rollback()
        return {"error": f"Invalid value: {ve}"}, 400

    except Exception as ex:
        db.session.rollback()
        return jsonify({"error": f"Unexpected error: {ex}"}), 500


@users_bp.route("/users/<int:pk>", methods=["GET"])
def get_user(pk):
    """Get a user by ID."""

    user = User.query.get(pk)

    if not user:
        return (
            jsonify({"message": f"User with id {pk} not found"}),
            404,
        )

    return jsonify(user.serialize()), 200


@users_bp.route("/users/<int:pk>", methods=["PUT"])
@jwt_required()
def update_user(pk):
    """Update a user by ID."""

    user = User.query.get(pk)

    if not user:
        return jsonify({"message": f"User with id {pk} not found"}), 404

    current_user_id = get_jwt_identity()

    if current_user_id != user.id:
        return jsonify({"message": "You can only update your own account"}), 403

    data = request.json
    user.username = data.get("username", user.username).strip()
    user.email = data.get("email", user.email).strip()

    if "password" in data:
        user.set_password(data.get("password"))

    db.session.commit()
    return jsonify(user.serialize()), 200


@users_bp.route("/users/<int:pk>", methods=["DELETE"])
@jwt_required()
def delete_user(pk):
    """Delete a user by ID."""

    try:
        user = User.query.get(pk)

        if not user:
            return jsonify({"message": f"User with id {pk} not found"}), 404

        current_user_id = get_jwt_identity()

        if current_user_id != user.id:
            return jsonify({"message": "You can only delete your own account"}), 403

        db.session.delete(user)
        db.session.commit()

        return jsonify({"message": f"User with id {pk} deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return (
            jsonify({"message": f"An error occurred while deleting the user {str(e)}"}),
            500,
        )


@users_bp.route("/users/<int:pk>/projects", methods=["GET"])
def get_user_projects(pk):
    """Get user projects."""

    user = User.query.get(pk)

    if not user:
        return jsonify({"message": f"User with id {pk} not found"}), 404

    projects = user.projects
    serialized_projects = [project.serialize() for project in projects]
    return jsonify(serialized_projects), 200


@users_bp.route("/users/<int:pk>/subscriptions", methods=["GET"])
def get_user_subscriptions(pk):
    """Get user subscriptions."""

    user = User.query.get(pk)

    if not user:
        return jsonify({"message": f"User with id {pk} not found"}), 404

    subscriptions = user.subscriptions
    serialized_subscriptions = [
        subscription.serialize() for subscription in subscriptions
    ]
    return jsonify(serialized_subscriptions), 200
