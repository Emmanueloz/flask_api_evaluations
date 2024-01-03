from flask import Blueprint, jsonify, request
from app.db.db_teachers import query_teacher, update_teacher, del_teacher
from app.roles import jwt_rol_required, ROL, current_user
from app.utils.data_teacher import response_teacher_json
bp = Blueprint("ApiTeacherProfile ", __name__,
               url_prefix="/api/teacher/profile")


@bp.get("/")
@jwt_rol_required([ROL.ADMIN, ROL.TEACHER])
def get_profile_teacher():
    try:
        id = current_user.id_teacher
        result = query_teacher(id)
        if result is None:
            return jsonify({"status": "error", "action": "query", "msg": "teacher not found"}), 404

        result = result.to_json()

        return jsonify({"status": "ok", "action": "query", "length": "1", "result": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 404


@bp.put("/")
@jwt_rol_required([ROL.ADMIN, ROL.TEACHER])
def put_profile_teacher():
    data = request.get_json()
    teacher_json, error = response_teacher_json(data)
    if error is not None:
        return jsonify({"status": "error", "action": "update", "msg": error}), 404

    id = current_user.id_teacher
    teacher = query_teacher(id)

    if teacher is None:
        return jsonify({"status": "error", "action": "update", "msg": "teacher not found"}), 404

    teacher = update_teacher(
        teacher, teacher_json["name"], teacher_json["subject"])

    return jsonify({"status": "ok", "action": "update", "length": "1", "result": teacher.to_json()}), 200
