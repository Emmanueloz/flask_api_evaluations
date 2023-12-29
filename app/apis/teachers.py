from flask import Blueprint, jsonify, request
from app.db.db_teachers import add_teacher, query_all_teachers, query_teacher
bp = Blueprint("ApiTeacher", __name__, url_prefix="/api/teacher")


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
        return jsonify({"status": "ok", "action": "query", "length": length, "result": result}), status_code
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 404


@bp.post("/")
def post_evaluation():
    data = request.get_json()
    name = data["name"]
    subject = data['subject']
    result = add_teacher(name, subject)

    return jsonify({"status": "ok", "action": "add", "length": "1", "result": result})


@bp.put("<id>")
def put_evaluation(id):
    data = {"id": id}
    return jsonify({"status": "ok", "action": "modify", "length": "1", "data": data})


@bp.delete("<id>")
def delete_evaluation(id):
    data = {"id": id}
    return jsonify({"status": "ok", "action": "delete", "length": "1", "data": data})
