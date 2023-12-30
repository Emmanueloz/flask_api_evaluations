from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from app.db.connection import db


class Evaluations(db.Model):
    id = Column(String(30), primary_key=True)
    title = Column(String(100))
    id_teacher = Column(Integer, ForeignKey("teacher.id"), nullable=False)

    # Definir la relación con Teacher
    teacher = relationship(
        'Teacher', backref=backref('evaluations', lazy=True))

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "teacher": self.teacher.to_json()  # Incluye los datos del maestro en la respuesta
        }

    def __init__(self, id, title, id_teacher) -> None:
        self.id = id
        self.title = title
        self.id_teacher = id_teacher
