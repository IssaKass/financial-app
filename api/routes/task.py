from flask import Blueprint, jsonify, request
from api.models import Task, User
from api.extensions import db
from flask_jwt_extended import jwt_required


tasks_bp = Blueprint("tasks", __name__, url_prefix="/api/v1/tasks")


def get_serialized_tasks():
    tasks = Task.query.all()
    serialized_tasks = [task.serialize() for task in tasks]
    return serialized_tasks


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    serialized_tasks = get_serialized_tasks()
    return jsonify(serialized_tasks), 200


@tasks_bp.route("", methods=["POST"])
@jwt_required()
def create_task():
    data = request.json

    required_fields = ["title", "project_id"]

    if not all(field in data for field in required_fields):
        return jsonify({"error:" "Required fields are missing"}), 400

    project_id = data["project_id"]

    if not User.query.get(project_id):
        return jsonify({"error": f"Project with id {project_id} does not exist"}), 404

    try:
        task = Task(
            title=data["title"].strip(),
            description=data["description"].strip(),
            project_id=data["project_id"],
        )
        task.completed = (
            bool(data["completed"]) if "completed" in data else task.completed
        )

        db.session.add(task)
        db.session.commit()

        return task.serialize(), 201

    except Exception as ex:
        db.session.rollback()
        return jsonify({"error": f"Failed to create task: {ex}"}), 500


@tasks_bp.route("/<int:pk>", methods=["GET"])
def get_task(pk):
    task = task.query.get(pk)

    if not task:
        return jsonify({"error": f"Task with id {pk} not found"}), 404

    return jsonify(task.serialize()), 200


@tasks_bp.route("/<int:pk>", methods=["PUT"])
@jwt_required()
def update_task(pk):
    task = Task.query.get(pk)

    if not task:
        return jsonify({"error": f"Task with id {pk} not found"}), 404

    data = request.json

    task.title = (
        str(data["title"]).strip() if "title" in data and data["title"] else task.title
    )
    task.description = (
        str(data["description"]).strip()
        if "description" in data and data["description"]
        else task.description
    )
    task.completed = bool(data["completed"]) if "completed" in data else task.completed

    db.session.commit()
    return jsonify(task.serialize()), 200


@tasks_bp.route("/<int:pk>", methods=["DELETE"])
@jwt_required()
def delete_task(pk):
    task = Task.query.get(pk)

    if not task:
        return jsonify({"error": f"task with id {pk} not found"}), 404

    db.session.delete(task)
    db.session.commit()

    serialized_tasks = get_serialized_tasks()
    return jsonify(serialized_tasks), 200
