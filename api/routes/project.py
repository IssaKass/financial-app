from flask import Blueprint, jsonify, request
from api.models import Project, ProjectStatus, User
from api.extensions import db
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

projects_bp = Blueprint("projects", __name__)


def get_serialized_projects():
    projects = Project.query.all()
    serialized_projects = [project.serialize() for project in projects]
    return serialized_projects


@projects_bp.route("/projects", methods=["GET"])
def get_all_projects():
    serialized_projects = get_serialized_projects()
    return jsonify(serialized_projects), 200


@projects_bp.route("/projects", methods=["POST"])
@jwt_required()
def create_project():
    data = request.json

    required_fields = ["name", "client", "budget", "start_date", "end_date", "user_id"]

    if not all(field in data for field in required_fields):
        return jsonify({"error:" "Required fields are missing"}), 400

    user_id = data["user_id"]

    if not User.query.get(user_id):
        return jsonify({"error": f"User with id {user_id} does not exist"}), 404

    try:
        name = data["name"].strip()

        existing_name = Project.query.filter_by(name=name).first()

        if existing_name:
            return jsonify({"error": {"name": "Project name already in use"}}), 400

        start_date = datetime.fromisoformat(data["start_date"])
        end_date = datetime.fromisoformat(data["end_date"])

        project = Project(
            name=name,
            client=data["client"].strip(),
            budget=data["budget"],
            start_date=start_date,
            end_date=end_date,
            user_id=data["user_id"],
        )
        project.images = (
            int(data["images"]) if "images" in data and data["images"] else 0
        )
        project.animation = (
            int(data["animation"]) if "animation" in data and data["animation"] else 0
        )
        project.status = (
            ProjectStatus[data["status"]]
            if "status" in data and data["status"]
            else ProjectStatus.PENDING
        )

        db.session.add(project)
        db.session.commit()

        return project.serialize(), 201

    except Exception as ex:
        db.session.rollback()
        return jsonify({"error": f"Failed to create project: {ex}"}), 500


@projects_bp.route("/projects/<int:pk>", methods=["GET"])
def get_project(pk):
    project = Project.query.get(pk)

    if not project:
        return jsonify({"error": f"Project with id {pk} not found"}), 404

    return jsonify(project.serialize()), 200


@projects_bp.route("/projects/<int:pk>", methods=["PUT"])
@jwt_required()
def update_project(pk):
    project = Project.query.get(pk)

    if not project:
        return jsonify({"error": f"Project with id {pk} not found"}), 404

    current_user_id = get_jwt_identity()

    if current_user_id != project.user_id:
        return jsonify({"error": "You can only update your own projects"}), 403

    data = request.json

    if "name" in data:
        existing_name = Project.query.filter_by(name=data["name"]).first()

        if existing_name and existing_name.id != pk:
            return jsonify({"error": {"name": "Project name already in use"}}), 400

    project.name = (
        str(data["name"]).strip() if "name" in data and data["name"] else project.name
    )
    project.client = (
        str(data["client"]).strip()
        if "client" in data and data["client"]
        else project.client
    )
    project.budget = (
        float(data["budget"]) if "budget" in data and data["budget"] else project.budget
    )
    project.images = (
        int(data["images"]) if "images" in data and data["images"] else project.images
    )
    project.animation = (
        int(data["animation"])
        if "animation" in data and data["animation"]
        else project.animation
    )
    project.status = (
        ProjectStatus[data["status"]]
        if "status" in data and data["status"]
        else project.status
    )

    db.session.commit()
    return jsonify(project.serialize()), 200


@projects_bp.route("/projects/<int:pk>", methods=["DELETE"])
@jwt_required()
def delete_project(pk):
    project = Project.query.get(pk)

    if not project:
        return jsonify({"error": f"Project with id {pk} not found"}), 404

    current_user_id = get_jwt_identity()

    if current_user_id != project.user_id:
        return jsonify({"error": "You can only delete your own projects"}), 403

    db.session.delete(project)
    db.session.commit()

    serialized_projects = get_serialized_projects()
    return jsonify(serialized_projects), 200
