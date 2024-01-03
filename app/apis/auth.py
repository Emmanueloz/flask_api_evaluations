from flask import Blueprint, request, jsonify
from app.db.db_users import add_user, query_user, query_all_users
from app.db.db_teachers import query_teacher
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token
from app.roles import jwt_rol_required, ROL
bp = Blueprint("AuthApi", __name__, url_prefix="/api/auth")


def response_user_json(data, email_required=True, rol_required=True, id_teacher_required=True):
    required_fields = ["username", "passwd"]

    if email_required:
        required_fields.append("email")
    if rol_required:
        required_fields.append("rol")
    if id_teacher_required:
        required_fields.append("id_teacher")

    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return None, f"{missing_fields[0]} is required"

    id_teacher = data["id_teacher"] if "id_teacher" in data else None

    if id_teacher is not None and query_teacher(id_teacher) is None:
        return None, "teacher not found"

    auth = {field: str(data[field]) for field in required_fields}

    return auth, None


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


@bp.post("/signup")
def sign_up():
    data = request.get_json()
    user, error = response_user_json(data)

    if error is not None:
        return jsonify({"status": "error", "action": "add", "msg": error}), 404

    passwd_hash = generate_password_hash(user["passwd"])

    user["passwd"] = passwd_hash

    response, error = add_user(user)

    if error is not None:
        return jsonify({"status": "error", "action": "add", "msg": error}), 500

    return jsonify({"status": "ok", "action": "add", "length": "1", "response": response})


@bp.post("/login")
def login():
    data = request.get_json()
    data, error = response_user_json(
        data, email_required=False, rol_required=False, id_teacher_required=False)

    if error is not None:
        return jsonify({"status": "error", "action": "add", "msg": error}), 500

    user, error = query_user(data["username"])

    if error is not None:
        return jsonify({"status": "error", "action": "add", "msg": error}), 500

    if not check_password_hash(user.passwd, data["passwd"]):
        return jsonify({"status": "error", "action": "add", "msg": "password not valid"}), 401

    access_token = create_access_token(identity=user)
    response = {
        "user": user.to_json(),
        "access_token": access_token
    }

    return jsonify({"status": "ok", "action": "add", "length": "1", "response": response})
