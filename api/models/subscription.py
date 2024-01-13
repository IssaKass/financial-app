"""
Subscription Model

This module defines the Subscription class, which represents a subscription in the application.

Attributes:
    id (int): The unique identifier for the subscription.
    name (str): The name of the subscription.
    website (str): The website associated with the subscription.
    price (float): The price of the subscription.
    start_date (datetime): The start date of the subscription.
    end_date (datetime): The end date of the subscription.
    active (bool): Indicates whether the subscription is currently active.
    created_at (datetime): The timestamp indicating when the subscription was created.
    updated_at (datetime): The timestamp indicating when the subscription was last updated.

Relationships:
    user (relationship): Many-to-One relationship with the User model.

Methods:
    __init__: Constructor method to initialize a new Subscription instance.
    __repr__: Representation method for the Subscription instance.
    serialize: Method to serialize the Subscription instance into a dictionary.

Example Usage:
    subscription = Subscription(
        name="Premium Plan",
        website="example.com",
        price=19.99,
        active=True,
        start_date=datetime(2022, 1, 1),
        end_date=datetime(2022, 12, 31),
        user_id=1
    )
    db.session.add(subscription)
    db.session.commit()

"""

from flask import url_for
from sqlalchemy.sql import func
from api.extensions import db


class Subscription(db.Model):
    """Subscription Model Class"""

    __tablename__ = "subscriptions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False, nullable=False)
    website = db.Column(db.String, nullable=False)
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    active = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", name="fk_subscription_user_id"),
        nullable=False,
    )

    user = db.relationship("user.User", backref="subscription_user")

    def __init__(self, name, website, price, start_date, end_date, user_id) -> None:
        """Subscription Constructor Method"""

        if start_date > end_date:
            raise ValueError("End date must be after start date")

        self.name = name
        self.website = website
        self.price = price
        self.start_date = start_date
        self.end_date = end_date
        self.user_id = user_id

    def __repr__(self) -> str:
        """Representation Method"""

        return f"<Subscription '{self.name}'>"

    def serialize(self) -> dict:
        """Serialize Method"""

        return {
            "id": self.id,
            "name": self.name,
            "website": self.website,
            "price": self.price,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "active": self.active,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "user": {
                "id": self.user_id,
                "url": url_for("users.get_user", pk=self.user_id),
            },
        }
