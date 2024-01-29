from flask import Blueprint, jsonify, request
from api.models import User, Subscription
from api.extensions import db
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

subscriptions_bp = Blueprint("subscriptions", __name__, url_prefix="/api/v1/subscriptions")


def get_serialized_subscriptions():
    subscriptions = Subscription.query.all()
    serialized_subscriptions = [
        subscription.serialize() for subscription in subscriptions
    ]
    return serialized_subscriptions


@subscriptions_bp.route("", methods=["GET"])
def get_all_subscriptions():
    serialized_subscriptions = get_serialized_subscriptions()
    return jsonify(serialized_subscriptions), 200


@subscriptions_bp.route("", methods=["POST"])
@jwt_required()
def create_subscription():
    data = request.json

    required_fields = ["name", "website", "price", "start_date", "end_date", "user_id"]

    if not all(field in data for field in required_fields):
        return jsonify({"error:" "Required fields are missing"}), 400

    user_id = data["user_id"]

    if not User.query.get(user_id):
        return jsonify({"error": f"User with id {user_id} does not exist"}), 404

    try:
        start_date = datetime.strptime(data["start_date"], "%Y-%m-%dT%H:%M:%S.%fZ")
        end_date = datetime.strptime(data["end_date"], "%Y-%m-%dT%H:%M:%S.%fZ")

        subscription = Subscription(
            name=data["name"].strip(),
            website=data["website"].strip(),
            price=data["price"],
            start_date=start_date,
            end_date=end_date,
            user_id=data["user_id"],
        )
        subscription.active = (
            bool(data["active"]) if "active" in data and data["active"] else False
        )

        db.session.add(subscription)
        db.session.commit()

        return subscription.serialize(), 201

    except Exception as ex:
        db.session.rollback()
        return jsonify({"error": f"Failed to create subscription: {ex}"}), 500


@subscriptions_bp.route("/<int:pk>", methods=["GET"])
def get_subscription(pk):
    subscription = Subscription.query.get(pk)

    if not subscription:
        return jsonify({"error": f"Subscription with id {pk} not found"}), 404

    return jsonify(subscription.serialize()), 200


@subscriptions_bp.route("/<int:pk>", methods=["PUT"])
@jwt_required()
def update_subscription(pk):
    subscription = Subscription.query.get(pk)

    if not subscription:
        return jsonify({"error": f"Subscription with id {pk} not found"}), 404

    current_user_id = get_jwt_identity()

    if current_user_id != subscription.user_id:
        return jsonify({"error": "You can only update your own subscriptions"}), 403

    data = request.json
    subscription.name = (
        str(data["name"]).strip()
        if "name" in data and data["name"]
        else subscription.name
    )
    subscription.website = (
        str(data["website"]).strip()
        if "website" in data and data["website"]
        else subscription.website
    )
    subscription.price = float(data["price"]) if "price" in data else subscription.price
    subscription.active = (
        bool(data["active"]) if "active" in data else subscription.active
    )
    subscription.start_date = (
        datetime.strptime(data["start_date"], "%Y-%m-%dT%H:%M:%S.%fZ")
        if "start_date" in data
        else subscription.start_date
    )
    subscription.end_date = (
        datetime.strptime(data["end_date"], "%Y-%m-%dT%H:%M:%S.%fZ")
        if "end_date" in data
        else subscription.end_date
    )

    db.session.commit()
    return jsonify(subscription.serialize()), 200


@subscriptions_bp.route("/<int:pk>", methods=["DELETE"])
@jwt_required()
def delete_subscription(pk):
    subscription = Subscription.query.get(pk)

    if not subscription:
        return jsonify({"error": f"Subscription with id {pk} not found"}), 404

    current_user_id = get_jwt_identity()

    if current_user_id != subscription.user_id:
        return jsonify({"error": "You can only delete your own subscriptions"}), 403

    db.session.delete(subscription)
    db.session.commit()

    serialized_subscriptions = get_serialized_subscriptions()
    return jsonify(serialized_subscriptions), 200
