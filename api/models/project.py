"""
Project Model

This module defines the Project class, which represents a project in the application.

Attributes:
    id (int): The unique identifier for the project.
    name (str): The name of the project.
    client (str): The client associated with the project.
    budget (float): The budget allocated for the project.
    images (int): The number of images related to the project.
    animation (int): The number of animations related to the project.
    start_date (datetime): The start date of the project.
    end_date (datetime): The end date of the project.
    created_at (datetime): The timestamp indicating when the project was created.
    updated_at (datetime): The timestamp indicating when the project was last updated.

Relationships:
    user (relationship): Many-to-One relationship with the User model.

Methods:
    __init__: Constructor method to initialize a new Project instance.
    __repr__: Representation method for the Project instance.
    serialize: Method to serialize the Project instance into a dictionary.

Example Usage:
    project = Project(
        name="Sample Project",
        client="Sample Client",
        budget=10000.0,
        images=5,
        animation=2,
        start_date=datetime(2022, 1, 1),
        end_date=datetime(2022, 12, 31),
        user_id=1
    )
    db.session.add(project)
    db.session.commit()
"""

from enum import Enum
from flask import url_for
from sqlalchemy.sql import func
from api.extensions import db


class ProjectStatus(str, Enum):
    PENDING = "PENDING"
    PROGRESS = "PROGRESS"
    FINISHED = "FINISHED"


class Project(db.Model):
    """Project Model Class"""

    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    client = db.Column(db.String, nullable=False)
    budget = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    images = db.Column(db.Integer, nullable=True, default=0)
    animation = db.Column(db.Integer, nullable=True, default=0)
    status = db.Column(db.Enum(ProjectStatus), default=ProjectStatus.PENDING)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user = db.relationship("user.User", back_populates="projects")

    tasks = db.relationship(
        "task.Task",
        back_populates="project",
        cascade="all, delete-orphan",
    )

    def __init__(
        self,
        name,
        client,
        budget,
        start_date,
        end_date,
        user_id,
    ) -> None:
        """Project Constructor Method"""

        if start_date > end_date:
            raise ValueError("End date must be after start date")

        self.name = name
        self.client = client
        self.budget = budget
        self.start_date = start_date
        self.end_date = end_date
        self.user_id = user_id

    def __repr__(self) -> str:
        """Representation Method"""

        return f"<Project '{self.name}'>"

    def serialize(self) -> dict:
        """Serialize Method"""

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "client": self.client,
            "budget": self.budget,
            "images": self.images,
            "animation": self.animation,
            "status": self.status,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "user": {
                "id": self.user_id,
                "url": url_for("users.get_user", pk=self.user_id),
            },
            "tasks_url": url_for("projects.get_project_tasks", pk=self.id),
        }
