"""
User Model

This module defines the User class, which represents a user in the application.

Attributes:
    id (int): The unique identifier for the user.
    username (str): The unique username for the user.
    email (str): The unique email address for the user.
    password_hash (str): The hashed password for the user.
    created_at (datetime): The timestamp indicating when the user was created.
    updated_at (datetime): The timestamp indicating when the user was last updated.

Relationships:
    projects (relationship): One-to-Many relationship with the Project model.
    subscriptions (relationship): One-to-Many relationship with the Subscription model.

Methods:
    __init__: Constructor method to initialize a new User instance.
    __repr__: Representation method for the User instance.
    set_password: Method to set the password for the user by generating a hash.
    check_password: Method to check if a provided password matches the stored hash.
    serialize: Method to serialize the User instance into a dictionary.

Example Usage:
    user = User(username="john_doe", email="john@example.com", password="secure_password")
    db.session.add(user)
    db.session.commit()
"""


from sqlalchemy.sql import func
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
from api.extensions import db


class User(db.Model):
    """User Model Class"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    projects = db.relationship(
        "project.Project", backref="user_projects", cascade="all, delete-orphan"
    )
    subscriptions = db.relationship(
        "subscription.Subscription",
        backref="user_subscriptions",
        cascade="all, delete-orphan",
    )

    def __init__(self, username, email, password):
        """User Constructor Method"""

        self.username = username
        self.email = email
        self.set_password(password)

    def __repr__(self):
        """Representation Method"""

        return f"<User '{self.username}'>"

    def set_password(self, password):
        """Set Password Method"""

        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check Password Method"""

        return check_password_hash(self.password_hash, password)

    def serialize(self):
        """Serialize Method"""

        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "projects_url": url_for("users.get_user_projects", pk=self.id),
            "subscriptions_url": url_for("users.get_user_subscriptions", pk=self.id),
        }
