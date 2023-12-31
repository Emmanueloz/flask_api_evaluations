from flask import Blueprint, jsonify, request
from app.services.evaluations import get_evaluation_json, add_evaluation_json, delete_evaluation_json, update_evaluation_json
from app.db.db_evaluations import add_evaluation, del_evaluation, query_all_evaluations, update_evaluation, query_evaluation
from app.db.db_teachers import query_name_teacher, query_teacher

bp = Blueprint("ApiEvaluation", __name__, url_prefix="/api/evaluation")


def response_evaluation_json(data):
    if "id_teacher" not in data or "evaluation_json" not in data:
        return None, "id_teacher and evaluation_json required"

    if not str(data["id_teacher"]).isdigit():
        return None, "Id teacher must be integer number"

    teacher_name = query_name_teacher(data["id_teacher"])
    if teacher_name is None:
        return None, "Not found teacher"

    evaluation_json: dict = data["evaluation_json"]

    if type(evaluation_json) != dict:
        return None, "evaluation_json not is a json"

    if "title" not in evaluation_json:
        return None, "Title is required in evaluate_json"

    evaluation = {
        "title": evaluation_json["title"],
        "id_teacher": data["id_teacher"],
        "teacher_name": teacher_name,
        "evaluation_json": data["evaluation_json"]
    }
    return evaluation, None


@bp.get("/")
def get_evaluations():
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))

        page = max(page, 1)
        limit = max(limit, 1)
        result, length = query_all_evaluations(page=page, limit=limit)
        return jsonify({"status": "ok", "action": "query all", "length": length, "result": result}), 200

    except ValueError as e:
        return jsonify({"status": "error", "message": "Invalid offset or limit value"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 404


@bp.get("<id>")
def get_evaluation(id):
    result: dict = get_evaluation_json(id)

    if result is None:
        return jsonify({"status": "ok", "action": "query", "length": 0, "result": result}), 404

    teacher = query_teacher(result["id_teacher"])

    if teacher is None:
        return jsonify({"status": "error", "action": "query", "msg": "teacher not found"}), 404

    result.pop("id_teacher")

    result["teacher"] = teacher.to_json()
    result['id'] = id

    return jsonify({"status": "ok", "action": "query", "length": 1, "result": result}), 200


@bp.post("/")
def post_evaluation():
    data = request.get_json()
    evaluation, error = response_evaluation_json(data)
    if error is not None:
        return jsonify({"status": "error", "action": "add", "msg": error}), 404

    evaluation_json: dict = evaluation["evaluation_json"]
    evaluation_json["id_teacher"] = evaluation["id_teacher"]

    response_firebase = add_evaluation_json(evaluation["evaluation_json"])
    evaluation["id"] = response_firebase["name"]
    add_evaluation(
        response_firebase["name"], evaluation_json["title"], evaluation["id_teacher"])

    return jsonify({"status": "ok", "action": "add", "length": "1", "response": evaluation})


@bp.put("<id>")
def put_evaluation(id):
    data = request.get_json()

    evaluation = query_evaluation(id)
    if evaluation is None:
        return jsonify({"status": "error", "action": "update", "msg": "evaluation not found"}), 404

    evaluation_dict, error = response_evaluation_json(data)

    if error is not None:
        return jsonify({"status": "error", "action": "update", "msg": error}), 404

    evaluation_json = evaluation_dict["evaluation_json"]
    evaluation_json["id_teacher"] = evaluation_dict["id_teacher"]

    update_evaluation_json(id, evaluation_json)

    update_evaluation(
        evaluation, evaluation_dict["id_teacher"], evaluation_dict["title"])

    return jsonify({"status": "ok", "action": "update", "length": "1", "response": evaluation_dict})


@bp.delete("<id>")
def delete_evaluation(id):
    response, error = del_evaluation(id)
    if error is not None:
        return jsonify({"status": "error", "action": "delete", "msg": error}), 404

    result = get_evaluation_json(id)
    status_code = delete_evaluation_json(id)
    return jsonify({"status": "ok", "action": "delete", "length": "1", "data": result}), status_code
