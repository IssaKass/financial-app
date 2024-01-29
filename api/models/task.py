from flask import url_for
from api.extensions import db


class Task(db.Model):
    """Task Model Class"""

    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False)

    project_id = db.Column(
        db.Integer, db.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    project = db.relationship("project.Project", back_populates="tasks")

    def __init__(
        self,
        title,
        description,
        project_id,
    ) -> None:
        """Task Constructor Method"""

        self.title = title
        self.description = description
        self.project_id = project_id

    def __repr__(self) -> str:
        """Representation Method"""

        return f"<Task '{self.title}'>"

    def serialize(self) -> dict:
        """Serialize Method"""

        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "project": {
                "id": self.project_id,
                "url": url_for("projects.get_project", pk=self.project_id),
            },
        }
