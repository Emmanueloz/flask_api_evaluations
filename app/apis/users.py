from flask import Blueprint, request, jsonify
from app.db.db_users import add_user, query_user, query_all_users
from app.roles import jwt_rol_required, ROL

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
