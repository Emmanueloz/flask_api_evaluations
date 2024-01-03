from flask import Blueprint, request, jsonify
from app.db.db_users import add_user, query_user
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from app.roles import jwt_rol_required, ROL
from app.utils.data_user import response_user_json

bp = Blueprint("AuthApi", __name__, url_prefix="/api/auth")


@bp.post("/signup")
def sign_up():
    data = request.get_json()
    user, error = response_user_json(data)

    roles = [ROL.TEACHER, ROL.STUDENT]

    if error is not None:
        return jsonify({"status": "error", "action": "add", "msg": error}), 400

    if user["rol"] == ROL.ADMIN or user["rol"] not in roles:
        return jsonify({"status": "error", "action": "add", "msg": "invalid role"}), 401

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
        return jsonify({"status": "error", "action": "add", "msg": error}), 400

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
