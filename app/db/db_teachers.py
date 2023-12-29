from app.db.connection import db
from app.models.md_teachers import Teacher


def add_teacher(name, subject):
    newTeacher = Teacher(name, subject)
    db.session.add(newTeacher)
    db.session.commit()

    return newTeacher.to_json()
