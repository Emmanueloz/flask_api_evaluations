from flask import Blueprint, jsonify

bp = Blueprint("ApiEvaluation", __name__, url_prefix="/api/evaluation")


@bp.get("/")
def get_evaluations():
    data = [{"id": "1"}]
    return jsonify({"status": "ok", "action": "query all", "length": "10", "data": data}), 200


@bp.get("<id>")
def get_evaluation(id):
    data = {"id": id}
    return jsonify({"status": "ok", "action": "query", "length": "1", "data": data})


@bp.post("<id>")
def post_evaluation(id):
    data = {"id": id}
    return jsonify({"status": "ok", "action": "add", "length": "1", "data": data})


@bp.put("<id>")
def put_evaluation(id):
    data = {"id": id}
    return jsonify({"status": "ok", "action": "modify", "length": "1", "data": data})


@bp.delete("<id>")
def delete_evaluation(id):
    data = {"id": id}
    return jsonify({"status": "ok", "action": "delete", "length": "1", "data": data})
