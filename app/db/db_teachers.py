from app.db.connection import db
from app.models.md_teachers import Teacher


def add_teacher(name, subject):
    newTeacher = Teacher(name, subject)
    db.session.add(newTeacher)
    db.session.commit()

    return newTeacher.to_json()


def query_all_teacher(page, limit):
    result = Teacher.query.paginate(page=page, per_page=limit)
    items = [item.to_json() for item in result.items]
    length = len(items)
    return items, length
