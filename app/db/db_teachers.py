from app.db.connection import db
from app.models.md_teachers import Teacher


def add_teacher(name, subject):
    new_teacher = Teacher(name, subject)
    db.session.add(new_teacher)
    db.session.commit()

    return new_teacher.to_json()


def query_all_teachers(page, limit):
    result = Teacher.query.paginate(page=page, per_page=limit)
    items = [item.to_json() for item in result.items]
    length = len(items)
    return items, length


def query_teacher(id):
    teacher: Teacher = Teacher.query.get(id)
    return teacher if teacher is not None else None


def query_name_teacher(id):
    teacher_name = Teacher.query.filter(
        Teacher.id == id).value(Teacher.name)

    return teacher_name


def update_teacher(teacher: Teacher, name: str, subject: str):
    teacher.name = name
    teacher.subject = subject
    db.session.commit()
    return teacher


def delete_teacher(id):
    teacher: Teacher = query_teacher(id)
    if teacher is None:
        return None, "The teacher didn't find"

    if teacher.evaluations:
        return None, "You can't eliminate the teacher because he has associated evaluations"

    db.session.delete(teacher)
    db.session.commit()
    return teacher, None
