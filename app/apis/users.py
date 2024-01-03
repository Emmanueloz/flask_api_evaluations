from flask import Blueprint, request, jsonify
from app.db.db_users import add_user, query_user, query_all_users, update_teacher
from app.roles import jwt_rol_required, ROL
from app.utils.data_user import response_user_json

bp = Blueprint("UserApi", __name__, url_prefix="/api/user")


@bp.get("/")
@jwt_rol_required([ROL.ADMIN])
def get_users():
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        # Verificar que offset y limit no sean negativos
        page = max(page, 1)
        limit = max(limit, 1)
        result, length = query_all_users(page=page, limit=limit)
        return jsonify({"status": "ok", "action": "query all", "length": length, "result": result}), 200

    except ValueError as e:
        return jsonify({"status": "error", "message": "Invalid offset or limit value"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 404


@bp.get("<id>")
@jwt_rol_required([ROL.ADMIN, ROL.TEACHER])
def get_user(id):

    teacher, error = query_user(id)

    if teacher is None:
        return jsonify({"status": "error", "action": "query", "msg": error}), 404

    return jsonify({"status": "ok", "action": "query", "length": 1, "result": teacher.to_json()}), 200


@bp.post("/")
@jwt_rol_required([ROL.ADMIN])
def post_user():
    try:
        data = request.get_json()
        user_dic, error = response_user_json(data, id_teacher_required=False)

        roles = [ROL.TEACHER, ROL.STUDENT, ROL.ADMIN]

        if error is not None:
            return jsonify({"status": "error", "action": "add", "message": error}), 400

        if user_dic["rol"] not in roles:
            return jsonify({"status": "error", "action": "add", "msg": "invalid role"}), 401

        user, error = add_user(user_dic)

        if error is not None:
            return jsonify({"status": "error", "action": "add", "message": error}), 400

        return jsonify({"status": "ok", "action": "add", "result": user}), 201
    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": str(e)}), 400


@bp.put("<id>")
@jwt_rol_required([ROL.ADMIN])
def put_user(id):
    try:
        data = request.get_json()
        user_dic, error = response_user_json(data)
        if error is not None:
            return jsonify({"status": "error", "action": "update", "message": error}), 400

        teacher, error = update_teacher(id, user_dic)

        if error is not None:
            return jsonify({"status": "error", "action": "update", "message": error}), 400

        return jsonify({"status": "ok", "action": "update", "result": teacher.to_json()}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400
