from app.db.connection import db
from app.models.md_evaluations import Evaluations


def add_evaluation(id, title, id_teacher):
    new_evaluation = Evaluations(id, title, id_teacher)
    db.session.add(new_evaluation)
    db.session.commit()
    return new_evaluation.to_json()


def query_all_evaluations(page, limit):
    result = Evaluations.query.paginate(page=page, per_page=limit)
    items = [item.to_json() for item in result.items]
    length = len(items)
    return items, length


def query_evaluation(id):
    evaluation: Evaluations = Evaluations.query.get(id)
    return evaluation if evaluation is not None else None


def update_evaluation(evaluation: Evaluations, id_teacher: int, title: str):
    evaluation.id_teacher = id_teacher
    evaluation.title = title
    db.session.commit()
    return evaluation


def del_evaluation(id):
    evaluation: Evaluations = query_evaluation(id)
    if evaluation is None:
        return None, "evaluation not found"

    db.session.delete(evaluation)
    db.session.commit()
    return evaluation, None
