"""
Authentication Blueprint for Flask application.

This module defines the authentication blueprint for user registration, 
login, and user information retrieval.

Endpoints:
    - /auth/register: Endpoint for user registration.
    - /auth/login: Endpoint for user login.
    - /auth/user: Endpoint to get the current user's information.

Functions:
    - get_current_user: Get the current user based on the identity in the JWT.

Example Usage:
    - To register a new user: POST /auth/register
    - To log in as a user: POST /auth/login
    - To get the current user's information: GET /auth/user
"""

import requests
from flask import Blueprint, jsonify, request, url_for
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from api.models import User

# Create a Blueprint for authentication
auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


def get_current_user():
    """Get the current user based on the identity in the JWT."""

    current_user_id = get_jwt_identity()
    return User.query.get(current_user_id)


@auth_bp.route("/login", methods=["POST"])
def login():
    """Endpoint for user login."""

    data = request.json

    required_fields = ["email", "password"]

    if not all(field in data for field in required_fields):
        return (
            jsonify({"message": "Email and password are required"}),
            400,
        )

    email = data["email"]
    password = data["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": {"email": "User with this email does not exist"}}), 401

    if not user.check_password(password):
        return jsonify({"error": {"password": "Invalid password"}}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({"userToken": access_token, "user": user.serialize()}), 200


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_user_profile():
    """Endpoint to get the current user's information."""

    user = get_current_user()

    if user:
        return jsonify(user.serialize()), 200

    return jsonify({"error": "User not found"}), 404
