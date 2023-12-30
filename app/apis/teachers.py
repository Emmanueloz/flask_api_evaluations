from flask import Blueprint, jsonify, request
from app.db.db_teachers import add_teacher, query_all_teachers, query_teacher, update_teacher, delete_teacher
bp = Blueprint("ApiTeacher", __name__, url_prefix="/api/teacher")


def get_teacher_json(data):
    if "name" not in data or "subject" not in data:
        return None, "name and subject required"

    teacher = {
        "name": data["name"],
        "subject": data["subject"]
    }
    return teacher, None


@bp.get("/")
def get_evaluations():
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        # Verificar que offset y limit no sean negativos
        page = max(page, 1)
        limit = max(limit, 1)
        result, length = query_all_teachers(page=page, limit=limit)
        return jsonify({"status": "ok", "action": "query all", "length": length, "result": result}), 200

    except ValueError as e:
        return jsonify({"status": "error", "message": "Invalid offset or limit value"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 404


@bp.get("<id>")
def get_evaluation(id):
    try:
        id = int(id)
        result = query_teacher(id)
        length = 1 if result is not None else 0
        status_code = 200 if result is not None else 404
        result = result.to_json() if result is not None else None

        return jsonify({"status": "ok", "action": "query", "length": length, "result": result}), status_code
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 404


@bp.post("/")
def post_evaluation():
    data = request.get_json()
    teacher, error = get_teacher_json(data)

    if error is not None:
        return jsonify({"status": "error", "action": "add", "msg": error}), 404

    result = add_teacher(teacher["name"], teacher['subject'])

    return jsonify({"status": "ok", "action": "add", "length": "1", "result": result}), 200


@bp.put("<id>")
def put_evaluation(id):
    data = request.get_json()

    teacher = query_teacher(id)

    if teacher is None:
        return jsonify({"status": "error", "action": "update", "msg": "user not found"}), 404

    teacher_dic, error = get_teacher_json(data)

    if error is not None:
        return jsonify({"status": "error", "action": "update", "msg": error}), 404

    result = update_teacher(
        teacher, teacher_dic["name"], teacher_dic["subject"])

    result = result.to_json()
    return jsonify({"status": "ok", "action": "update", "length": "1", "result": result})


@bp.delete("<id>")
def delete_evaluation(id):
    result = delete_teacher(id)
    if result is None:
        return jsonify({"status": "error", "action": "delete", "msg": "user not found"}), 404
    result = result.to_json()
    return jsonify({"status": "ok", "action": "delete", "length": "1", "result": result})
