from flask import Blueprint, jsonify, request
from app.db.db_teachers import add_teacher
bp = Blueprint("ApiTeacher", __name__, url_prefix="/api/teacher")


@bp.get("/")
def get_evaluations():
    data = [{"id": "1", "name": "maestro"}]
    return jsonify({"status": "ok", "action": "query all", "length": "10", "data": data}), 200


@bp.get("<id>")
def get_evaluation(id):
    data = {"id": id}
    return jsonify({"status": "ok", "action": "query", "length": "1", "data": data})


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